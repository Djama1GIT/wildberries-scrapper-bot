import logging

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common.schemas.users import User
from bot.database.exceptions import DatabaseError
from bot.database.models.users import User
from bot.database.repositories import handle_exceptions


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_language_code(self, user_id: int) -> str:
        try:
            logging.info(f"Fetching language code for user {user_id}")

            select_stmt = select(User.language_code).where(User.user_id == user_id)
            result = await self.session.execute(select_stmt)
            language_code = result.scalars().first()

            logging.info(f"Fetched language code({language_code}) for user {user_id}")
            return language_code
        except SQLAlchemyError as exc:
            logging.error(f"Error fetching language code for user {user_id}: {exc}")
            raise DatabaseError(exc)

    @handle_exceptions
    async def insert_or_update_user(self, user_id: int, language_code: str) -> None:
        logging.info(f"Inserting or updating user {user_id}, language code: {language_code}")

        select_user_stmt = select(User).where(User.user_id == user_id)
        user = await self.session.execute(select_user_stmt)
        exist = user.first()

        if exist:
            update_user_stmt = update(User).\
                where(User.user_id == user_id).\
                values(language_code=language_code)
            await self.session.execute(update_user_stmt)
            logging.info(f"Updating user {user_id}")
        else:
            new_record = User(user_id=user_id, language_code=language_code)
            self.session.add(new_record)
            logging.info(f"Inserting user {user_id}")

        await self.session.commit()
        logging.info(f"Inserted or updated user {user_id}")
