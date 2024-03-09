from aiogram import Router, types
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart

from bot.database.repositories.users import UsersRepository
from bot.filters import IsChatType
from bot.filters.users import InjectUsersRepositoryFilter
from bot.keyboards.main import get_main_kb
from bot.middlewares.i18n import gettext as _


def register_start(router: Router):
    router.message.register(
        start_message,
        CommandStart(),
        IsChatType(ChatType.PRIVATE),
        InjectUsersRepositoryFilter()
    )


async def start_message(msg: types.Message, users_repository: UsersRepository) -> None:
    reply_text = _("Hi, {}").format(msg.from_user.full_name)
    await users_repository.insert_or_update_user(msg.from_user.id, msg.from_user.language_code)
    await msg.answer(
        text=reply_text,
        reply_markup=get_main_kb(),
    )
