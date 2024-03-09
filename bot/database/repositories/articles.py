import logging
from typing import List

from sqlalchemy import select, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from bot.common.schemas import ArticlesHistoryReadSchema, ArticlesHistoryCreateSchema
from bot.database.models.articles import ArticlesHistory, ArticleUserSubscribes
from bot.database.exceptions import DatabaseError
from bot.database.repositories import handle_exceptions


class ArticlesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def select_history(self, user_id: int, limit: int = 5) -> List[ArticlesHistoryReadSchema]:
        try:
            logging.info(f"Fetching article history for user {user_id} with limit {limit}")
            select_stmt = select(ArticlesHistory). \
                where(ArticlesHistory.user_id == user_id). \
                order_by(desc(ArticlesHistory.id)). \
                limit(limit)

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

    async def check_user_is_subscribed_to_any(self, user_id):
        try:
            logging.info(f"Checking if user {user_id} is subscribed to any articles")
            select_stmt = select(ArticleUserSubscribes).where(ArticleUserSubscribes.user_id == user_id)
            history = await self.session.execute(select_stmt)
            is_subscribed = bool(history.fetchone())
            logging.info(f"User {user_id} {'is' if is_subscribed else 'is not'} subscribed to any articles")
            return is_subscribed
        except SQLAlchemyError as exc:
            logging.error(f"Error checking user subscription for user {user_id}: {exc}")
            raise DatabaseError(exc)

    @handle_exceptions
    async def insert_subscribe_record(self, user_id: int, article: int) -> None:
        logging.info(f"Inserting subscribe record for user {user_id} and article {article}")
        new_record = ArticleUserSubscribes(user_id=user_id, article=article)
        self.session.add(new_record)
        await self.session.commit()
        logging.info(f"Inserted subscribe record for user {user_id} and article {article}")

    @handle_exceptions
    async def delete_subscribe_records(self, user_id) -> None:
        logging.info(f"Deleting subscribe records for user {user_id}")
        delete_stmt = delete(ArticleUserSubscribes).where(ArticleUserSubscribes.user_id == user_id)
        await self.session.execute(delete_stmt)
        logging.info(f"Deleted subscribe records for user {user_id}")
