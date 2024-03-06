from aiogram import BaseMiddleware, Router


def register_middlewares(
        router: Router,
        *middlewares: BaseMiddleware,
        is_outer: bool
) -> None:
    if is_outer:
        for middleware in middlewares:
            router.message.outer_middleware.register(middleware)
            router.callback_query.outer_middleware.register(middleware)
    else:
        for middleware in middlewares:
            router.message.middleware.register(middleware)
            router.callback_query.middleware.register(middleware)
