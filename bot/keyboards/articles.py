from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.middlewares.i18n import gettext as _


def get_subscribe_to_the_article_ikb() -> InlineKeyboardMarkup:
    """
    Subscribe to the article
    :return: InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Subscribe"), callback_data="subscribe"),
            ],
        ]
    )

    return kb
