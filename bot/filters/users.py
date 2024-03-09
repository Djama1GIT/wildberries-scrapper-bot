from aiogram import types
from aiogram.filters import Filter

from bot.database import async_session_maker
from bot.database.repositories.users import UsersRepository


class InjectUsersRepositoryFilter(Filter):

    async def __call__(self, message: types.Message):
        async_session = async_session_maker()
        users_repository = UsersRepository(async_session)
        return {
            "users_repository": users_repository,
        }
