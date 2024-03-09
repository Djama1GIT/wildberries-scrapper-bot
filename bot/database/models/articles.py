from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models import Base


class ArticleUserSubscribes(Base):
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
    article: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )


class ArticlesHistory(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    article: Mapped[int] = mapped_column(BigInteger, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    name: Mapped[str]
    price: Mapped[float]
    rating: Mapped[float]
    quantity: Mapped[int]

    def as_dict(self):
        return {
            "name": self.name,
            "article": self.article,
            "price": self.price,
            "rating": self.rating,
            "quantity": self.quantity,
            "created_at": self.created_at,
        }
