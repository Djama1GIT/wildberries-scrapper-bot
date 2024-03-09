from bot.utils.wildberries.apiclient import get_card_details, serialize_card_details
from bot.common.schemas.articles import Product


def get_info_about_product(article: int | str) -> Product:
    data = get_card_details(article)
    serialized_data = serialize_card_details(data)

    return Product(**serialized_data)
