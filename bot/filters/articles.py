from aiogram import types
from aiogram.filters import Filter

from bot.database import async_session_maker
from bot.database.repositories.articles import ArticlesRepository


class InjectArticlesRepositoryFilter(Filter):

    async def __call__(self, message: types.Message):
        async_session = async_session_maker()
        articles_repository = ArticlesRepository(async_session)
        return {
            "articles_repository": articles_repository,
        }
