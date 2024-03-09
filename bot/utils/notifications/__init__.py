from celery import Celery

from bot.config import Settings

settings = Settings()

celery = Celery('notifications',
                broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")


@celery.task
def send_notifications_for_all():
    """
    This task generates other tasks for all products that users subscribed

    Returns:
        None
    """
    pass


@celery.task
def send_notifications_for_specific(article: int, users: list[int]):
    """
    Send a notification to users subscribed to a specific product

    Args:
        article: number
        users: List[user_id]

    Returns:
        None
    """
    pass
