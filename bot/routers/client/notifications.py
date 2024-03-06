from aiogram import Router, types, F

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


def register_notifications(router: Router):
    router.message.register(stop_notifications_message, F.text == __("Stop notifications"))


async def stop_notifications_message(msg: types.Message) -> None:
    await msg.answer(
        text="stop notifications",
    )
