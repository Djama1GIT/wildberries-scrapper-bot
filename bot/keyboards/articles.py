from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.middlewares.i18n import gettext as _


class SubscribeCallback(CallbackData, prefix="subscribe"):
    article: int


def get_subscribe_to_the_article_ikb(article: str | int) -> InlineKeyboardMarkup:
    """
    Subscribe to the article
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Subscribe"),
                    callback_data=SubscribeCallback(article=article).pack()
                ),
            ],
        ],
    )

    return kb
