from typing import Optional

from aiogram import Router

from bot.routers.client.articles import register_articles
from bot.routers.client.notifications import register_notifications
from bot.routers.client.start import register_start


def register_client_router(router: Optional[Router] = None) -> Router:
    if router is None:
        router = Router(name="client")

    register_start(router)

    register_articles(router)

    register_notifications(router)

    return router
