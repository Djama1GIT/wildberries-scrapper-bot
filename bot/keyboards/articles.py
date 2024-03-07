from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.middlewares.i18n import gettext as _


def subscribe_to_the_article() -> InlineKeyboardMarkup:
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
