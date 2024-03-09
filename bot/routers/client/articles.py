from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy.exc import IntegrityError

from bot.config import Settings
from bot.common.schemas import (
    ArticlesHistoryCreateSchema,
    ArticlesHistoryReadSchema,
)
from bot.common.schemas.articles import Product
from bot.database.repositories.articles import ArticlesRepository
from bot.filters.articles import InjectArticlesRepositoryFilter
from bot.keyboards.articles import get_subscribe_to_the_article_ikb, \
    SubscribeCallback
from bot.utils.wildberries.exceptions import (
    WildberriesError404,
)
import bot.utils.wildberries as wb

settings = Settings()


class GetArticleDataForm(StatesGroup):
    article = State()


def register_articles(router: Router) -> None:
    router.message.register(
        get_article_data_from_db_message,
        InjectArticlesRepositoryFilter(),
        F.text == __("Get information from the database"),
    )
    router.message.register(
        get_article_data_message,
        F.text == __("Get product information"),
    )
    router.message.register(
        get_article_data_by_number_message,
        InjectArticlesRepositoryFilter(),
        GetArticleDataForm.article,
    )
    router.callback_query.register(
        subscribe_to_the_article_callback,
        InjectArticlesRepositoryFilter(),
        SubscribeCallback.filter(),
    )


async def get_article_data_message(msg: types.Message,
                                   state: FSMContext) -> None:
    await state.set_state(GetArticleDataForm.article)
    await msg.answer(
        text=_("Which article's information do you want to receive?"),
    )


async def get_article_data_by_number_message(
        msg: types.Message,
        state: FSMContext,
        articles_repository: ArticlesRepository
) -> None:
    article = msg.text
    if article.isnumeric():
        try:
            product: Product = wb.get_info_about_product(article)
            await msg.answer(
                text=f"{_('Actual information')}\n\n"
                     f"{str(product)}",
                reply_markup=get_subscribe_to_the_article_ikb(article),
            )
            await articles_repository.insert_history_record(
                ArticlesHistoryCreateSchema(
                    user_id=msg.from_user.id,
                    **product.model_dump(),
                ),
            )
        except WildberriesError404:
            await msg.answer(
                text=_(
                    "It is impossible to get information about this article."),
            )
        except:
            await msg.answer(
                text=_(
                    "An error occurred while requesting data, please try again later.")
            )
    else:
        await msg.answer(
            text=_("The article number must be in numerical format."),
        )
    await state.clear()


async def get_article_data_from_db_message(
        msg: types.Message,
        state: FSMContext,
        articles_repository: ArticlesRepository
) -> None:
    try:
        history: list[ArticlesHistoryReadSchema] = \
            await articles_repository.select_history(msg.from_user.id)
        if history:
            await msg.answer(
                text=f"{_('Information from the database')}\n\n"
                     f"{''.join([str(record) for record in history])}",
            )
        else:
            await msg.answer(
                text=_("The request history is empty."),
            )
    except:
        await msg.answer(
            text=_(
                "An error occurred while requesting data, please try again later.")
        )
    finally:
        await state.clear()


async def subscribe_to_the_article_callback(
        call: types.CallbackQuery,
        callback_data: SubscribeCallback,
        articles_repository: ArticlesRepository
) -> None:
    await call.answer()
    try:
        await articles_repository.insert_subscribe_record(
            user_id=call.from_user.id,
            article=callback_data.article,
        )
        await call.message.answer(
            text=_("You have successfully subscribed to the product {}.").format(callback_data.article),
        )
    except IntegrityError:
        await call.message.answer(
            text=_("You have already subscribed to this product.")
        )
    except:
        await call.message.answer(
            text=_("An error has occurred. Try again later.")
        )
