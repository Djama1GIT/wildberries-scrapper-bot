from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.middlewares.i18n import gettext as _


def get_main_kb() -> ReplyKeyboardMarkup:
    """
    Get kb for main menu
    :return: ReplyKeyboardMarkup
    """
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Get information from the database")),
                KeyboardButton(text=_("Stop notifications"))
            ],
            [
                KeyboardButton(text=_("Get product information")),
            ]
        ]
    )

    return kb
