import logging
from collections import defaultdict
from typing import List

from sqlalchemy import select, delete, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common.schemas import (
    ArticlesHistoryReadSchema,
    ArticlesHistoryCreateSchema,
    ArticleSubscribers,
)
from bot.common.schemas.users import User
from bot.database.exceptions import DatabaseError, ExistenceError
from bot.database.models.articles import (
    ArticlesHistory,
    ArticleUserSubscribes,
)
from bot.database.repositories import handle_exceptions
from bot.database.repositories.users import UsersRepository


class ArticlesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def select_history(self, user_id: int, limit: int = 5) -> List[ArticlesHistoryReadSchema]:
        try:
            logging.info(f"Fetching article history for user {user_id}, limit: {limit}")

            select_stmt = select(ArticlesHistory) \
                .where(ArticlesHistory.user_id == user_id) \
                .order_by(desc(ArticlesHistory.id)) \
                .limit(limit)
            result = await self.session.execute(select_stmt)
            history = result.scalars().all()

            logging.info(f"Fetched {len(history)} articles for user {user_id}")
            return [ArticlesHistoryReadSchema(**item.as_dict()) for item in history]
        except SQLAlchemyError as exc:
            logging.error(f"Error fetching article history for user {user_id}: {exc}")
            raise DatabaseError(exc)

    @handle_exceptions
    async def insert_history_record(self, record: ArticlesHistoryCreateSchema) -> None:
        logging.info(f"Inserting article history record for user {record.user_id}")

        new_record = ArticlesHistory(**record.model_dump())
        self.session.add(new_record)
        await self.session.commit()

        logging.info(f"Inserted article history record for user {record.user_id}")

    async def check_is_user_subscribed_to_product(self, user_id: int, article: int):
        try:
            logging.info(f"Checking if user {user_id} is subscribed to product {article}")

            select_stmt = select(ArticleUserSubscribes) \
                .where((ArticleUserSubscribes.user_id == user_id) &
                       (ArticleUserSubscribes.article == article))
            history = await self.session.execute(select_stmt)
            is_subscribed = bool(history.fetchone())

            logging.info(f"User {user_id} {'is' if is_subscribed else 'is not'} subscribed to product {article}")
            return is_subscribed
        except SQLAlchemyError as exc:
            logging.error(
                f"Error checking user subscription for user {user_id}, product: {article}: {exc}")
            raise DatabaseError(exc)

    async def get_subscribers_for_all_articles(self) -> List[ArticleSubscribers]:
        logging.info("Search for subscribers by all articles")

        select_stmt = select(ArticleUserSubscribes)
        result = await self.session.execute(select_stmt)
        subscriptions = result.scalars().all()

        subscribers = defaultdict(list)
        for subscription in subscriptions:
            users_repository = UsersRepository(self.session)
            user_language = await users_repository.get_user_language_code(subscription.user_id)
            user = User(user_id=subscription.user_id, language_code=user_language)
            subscribers[subscription.article].append(user)

        logging.info(f"Fetched subscribers for {len(subscribers)} articles")
        return [ArticleSubscribers(article=article, users=users)
                for article, users in subscribers.items()]

    @handle_exceptions
    async def insert_subscribe_record(self, user_id: int, article: int) -> None:
        logging.info(f"Inserting subscribe record for user {user_id} and product {article}")

        new_record = ArticleUserSubscribes(user_id=user_id, article=article)
        self.session.add(new_record)
        await self.session.commit()

        logging.info(f"Inserted subscribe record for user {user_id} and product {article}")

    @handle_exceptions
    async def delete_subscribe_record(self, user_id: int, article: int) -> None:
        logging.info(f"Deleting subscribe record for user {user_id}, article {article}")

        delete_stmt = delete(ArticleUserSubscribes) \
            .where((ArticleUserSubscribes.user_id == user_id) &
                   (ArticleUserSubscribes.article == article))
        delete_result = await self.session.execute(delete_stmt)
        await self.session.commit()

        logging.info(f"Deleted subscribe record for user {user_id}, article: {article}")

        if not delete_result.rowcount:
            raise ExistenceError(f"The user is not subscribed to product {article}")

    @handle_exceptions
    async def delete_subscribe_records(self, user_id: int) -> None:
        logging.info(f"Deleting subscribe records for user {user_id}")

        delete_stmt = delete(ArticleUserSubscribes) \
            .where(ArticleUserSubscribes.user_id == user_id)
        delete_result = await self.session.execute(delete_stmt)
        await self.session.commit()

        logging.info(f"Deleted subscribe records for user {user_id}")

        if not delete_result.rowcount:
            raise ExistenceError("The user is not subscribed to any products")
