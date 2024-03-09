from aiogram import Router, types, F

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.database.exceptions import ExistenceError
from bot.database.repositories.articles import ArticlesRepository
from bot.filters.articles import InjectArticlesRepositoryFilter


def register_notifications(router: Router):
    router.message.register(
        stop_notifications_message,
        InjectArticlesRepositoryFilter(),
        F.text == __("Stop notifications")
    )


async def stop_notifications_message(
        msg: types.Message,
        articles_repository: ArticlesRepository
) -> None:
    try:
        await articles_repository.delete_subscribe_records(msg.from_user.id)
        await msg.answer(
            text=_("You have successfully unsubscribed from all products.")
        )
    except ExistenceError:
        await msg.answer(
            text=_("You are not subscribed to any products.")
        )
    except:
        await msg.answer(
            text=_("An error has occurred. Try again later.")
        )
