import asyncio
import logging

from aiogram import Bot
from celery import Celery

from bot.common.schemas.articles import Product
from bot.config import Settings
from bot.database import async_session_maker
from bot.database.repositories.articles import ArticlesRepository
import bot.utils.wildberries as wb
from bot.keyboards.articles import get_unsubscribe_to_the_article_ikb

from bot.middlewares.i18n import gettext as _

settings = Settings()

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(message)s"
    )

celery = Celery('bot.utils.notifications',
                broker="{driver}{host}:{port}".format(
                    driver="redis://",
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                ),
                include=["bot"])

celery.conf.beat_schedule = {
    'notifications': {
        'task': 'bot.utils.notifications.send_notifications_for_all',
        'schedule': settings.NOTIFICATION_PERIOD,
    },
}


@celery.task
def send_notifications_for_specific(subscribers: dict):
    async def wrapped():
        bot = Bot(token=settings.TOKEN)

        article = subscribers.get("article")
        product: Product = wb.get_info_about_product(article)

        for user in subscribers.get("users"):
            language_code = user.get("language_code")
            await bot.send_message(
                chat_id=user.get("user_id"),
                text=f"{_('Actual information', locale=language_code)}"
                     f"\n\n"
                     f"{_('Product name', locale=language_code)}: {product.name}\n"
                     f"{_('Article', locale=language_code)}: {product.article}\n"
                     f"{_('Price', locale=language_code)}: {product.price}\n"
                     f"{_('Rating', locale=language_code)}: {product.rating}\n"
                     f"{_('Quantity in stock', locale=language_code)}: {product.quantity}",
                reply_markup=get_unsubscribe_to_the_article_ikb(article, language_code)
            )
        await bot.session.close()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(wrapped())
    loop.close()
    return True


@celery.task
def send_notifications_for_all():
    async def wrapped():
        session = async_session_maker()
        articles_repository = ArticlesRepository(session)
        articles = await articles_repository.get_subscribers_for_all_articles()
        for article in articles:
            send_notifications_for_specific.delay(article.model_dump())
        await session.close()

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
    loop.run_until_complete(wrapped())
    return True
