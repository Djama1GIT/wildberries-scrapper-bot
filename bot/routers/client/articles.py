from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.keyboards.articles import get_subscribe_to_the_article_ikb
from bot.utils.wildberries.exceptions import WildberriesError404, WildberriesError500
import bot.utils.wildberries as wb


class SubscribeArticleForm(StatesGroup):
    article = State()
    article_db = State()


def register_articles(router: Router) -> None:
    router.message.register(get_article_data_from_db_message, F.text == __("Get information from the database"))
    router.message.register(get_article_data_message, F.text == __("Get product information"))
    router.message.register(get_article_data_by_number_message, SubscribeArticleForm.article)
    router.callback_query.register(subscribe_to_the_article_callback, F.data == "subscribe")


async def get_article_data_from_db_message(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(SubscribeArticleForm.article_db)
    await msg.answer(
        text=_("Which article's information do you want to receive?"),
    )


async def get_article_data_message(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(SubscribeArticleForm.article)
    await msg.answer(
        text=_("Which article's information do you want to receive?"),
    )


async def get_article_data_by_number_message(msg: types.Message, state: FSMContext) -> None:
    article = msg.text
    if article.isnumeric():
        try:
            data = wb.get_data_about_article(article)
            await msg.answer(
                text=f'{_("Product name")}: {data.get("name")}\n'
                     f'{_("Article")}: {data.get("article")}\n'
                     f'{_("Price")}: {data.get("price")}\n'
                     f'{_("Rating")}: {data.get("rating")}\n'
                     f'{_("Quantity in stock")}: {data.get("quantity")}',
                reply_markup=get_subscribe_to_the_article_ikb(),
            )
        except WildberriesError404:
            await msg.answer(
                text=_("It is impossible to get information about this article."),
            )
        except WildberriesError500:
            await msg.answer(
                text=_("An error occurred while requesting data, please try again later.")
            )
    else:
        await msg.answer(
            text=_("The article number must be in numerical format."),
        )
    await state.clear()


async def subscribe_to_the_article_callback(call: types.CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(
        text="subscribe to the article"
    )
