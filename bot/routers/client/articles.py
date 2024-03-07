from aiogram import Router, types, F

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.keyboards.articles import subscribe_to_the_article


def register_articles(router: Router):
    router.message.register(get_article_data_from_db_message, F.text == __("Get information from the database"))
    router.message.register(get_article_data_message, F.text == __("Get product information"))
    router.callback_query.register(subscribe_to_the_article_callback, F.data == "subscribe")


async def get_article_data_from_db_message(msg: types.Message) -> None:
    await msg.answer(
        text="get article data from db",
        reply_markup=subscribe_to_the_article(),
    )


async def get_article_data_message(msg: types.Message) -> None:
    await msg.answer(
        text="get article data",
        reply_markup=subscribe_to_the_article(),
    )


async def subscribe_to_the_article_callback(call: types.CallbackQuery) -> None:
    await call.answer(
        text="subscribe to the article"
    )
    await call.message.answer(
        text="subscribe to the article"
    )
