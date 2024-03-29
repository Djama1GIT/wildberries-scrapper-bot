from datetime import datetime

from typing import Optional, List

from pydantic import BaseModel, Field

from aiogram.utils.i18n import gettext as _

from bot.common.schemas.users import User


class Product(BaseModel):
    article: int = Field(..., description="Article of the product")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    rating: float = Field(..., description="Product rating")
    quantity: int = Field(..., description="Quantity in stock")

    def __str__(self):
        return f'{_("Product name")}: {self.name}\n' \
               f'{_("Article")}: {self.article}\n' \
               f'{_("Price")}: {self.price}\n' \
               f'{_("Rating")}: {self.rating}\n' \
               f'{_("Quantity in stock")}: {self.quantity}'


class ArticlesHistoryReadSchema(Product):
    id: Optional[int] = Field(None, description="Identifier of the record")
    user_id: Optional[int] = Field(None, description="User identifier")
    created_at: Optional[datetime] = Field(None,
                                           description="Record creation date")

    def __str__(self):
        return "{other_info}\n{datetime_caption}: {datetime}\n{sep}\n".format(
            other_info=str(Product(**self.model_dump())),
            datetime_caption=_("Record created at"),
            datetime=self.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            sep="=" * 30,
        )


class ArticlesHistoryCreateSchema(ArticlesHistoryReadSchema):
    user_id: int = Field(..., description="User identifier")


class ArticleSubscribers(BaseModel):
    article: int = Field(..., description="Article of the product")
    users: List[User] = Field(..., description="Users who subscribed")
