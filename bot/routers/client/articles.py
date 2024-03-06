from aiogram import Router, types, F

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


def register_articles(router: Router):
    router.message.register(get_article_data_from_db_message, F.text == __("Get information from the database"))
    router.message.register(get_article_data_message, F.text == __("Get product information"))


async def get_article_data_from_db_message(msg: types.Message) -> None:
    await msg.answer(
        text="get article data from db",
    )


async def get_article_data_message(msg: types.Message) -> None:
    await msg.answer(
        text="get article data"
    )
