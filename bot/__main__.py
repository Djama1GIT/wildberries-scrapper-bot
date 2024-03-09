import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties

from bot.config import Settings
from bot.middlewares import register_middlewares
from bot.middlewares.i18n import simple_locale_middleware
from bot.routers import register_routers
from bot.routers.client import register_client_router

settings = Settings()

bot = Bot(token=settings.TOKEN,
          default=DefaultBotProperties(parse_mode="HTML"))


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(message)s"
    )
    logging.info("Bot starting...")

    dp = Dispatcher()

    router = Router(name="main")
    register_routers(router, register_client_router())
    register_middlewares(router, simple_locale_middleware, is_outer=True)
    dp.include_router(router)

    try:
        await dp.start_polling(bot)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
