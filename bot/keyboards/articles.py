from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.middlewares.i18n import gettext as _


class SubscribeCallback(CallbackData, prefix="subscribe"):
    article: int


class UnsubscribeCallback(CallbackData, prefix="unsubscribe"):
    article: int


def get_subscribe_to_the_article_ikb(article: str | int, locale=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Subscribe", locale=locale),
                    callback_data=SubscribeCallback(article=article).pack()
                ),
            ],
        ],
    )

    return ikb


def get_unsubscribe_to_the_article_ikb(article: str | int, locale=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Unsubscribe", locale=locale),
                    callback_data=UnsubscribeCallback(article=article).pack()
                ),
            ],
        ],
    )

    return ikb
