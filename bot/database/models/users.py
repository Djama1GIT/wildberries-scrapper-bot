from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models import Base
from bot.config import Settings

settings = Settings()


class User(Base):
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
    language_code: Mapped[int] = mapped_column(
        String,
        nullable=False,
        default=settings.DEFAULT_LOCALE
    )
