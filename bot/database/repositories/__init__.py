import logging

from sqlalchemy.exc import SQLAlchemyError

from bot.database.exceptions import CommitError, RollbackError


def handle_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as exc:
            logging.error(f"SQLAlchemyError occurred in {func.__name__}: {exc}")
            try:
                logging.info(f"Attempting to rollback session due to SQLAlchemyError in {func.__name__}")
                await args[0].session.rollback()
                raise CommitError(exc)
            except SQLAlchemyError as exc:
                logging.error(f"RollbackError occurred in {func.__name__}: {exc}")
                raise RollbackError(exc)

    return wrapper
