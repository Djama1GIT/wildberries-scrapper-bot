from aiogram import Router, types
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart

from bot.filters import IsChatType
from bot.keyboards.main import get_main_kb
from bot.middlewares.i18n import gettext as _


def register_start(router: Router):
    router.message.register(start_message, CommandStart(), IsChatType(ChatType.PRIVATE))


async def start_message(msg: types.Message) -> None:
    reply_text = _("Hi, {}").format(msg.from_user.full_name)
    await msg.answer(
        text=reply_text,
        reply_markup=get_main_kb(),
    )
