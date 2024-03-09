import logging

import requests as requests

from bot.utils.wildberries.exceptions import WildberriesError, WildberriesError404, WildberriesError500


def get_card_details(article: int | str) -> dict:
    try:
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
        response = requests.get(url)
        data = response.json()
        products = data.get("data").get("products")
    except Exception as e:
        logging.error(e)
        raise WildberriesError500(f"An unexpected error has occurred while getting card details")

    if not products:
        raise WildberriesError404("This article does not exist.")

    return data


def serialize_card_details(card_details: dict) -> dict:
    try:
        data = card_details.get("data")
        product = data.get("products")[0]
        serialized_data = {
            "name": product.get("name"),
            "article": int(product.get("id")),
            "price": int(product.get("salePriceU")) / 100,
            "rating": float(product.get("reviewRating")),
            "quantity": 0,
        }

        for size in product.get("sizes"):
            for stock in size.get("stocks"):
                serialized_data["quantity"] += stock.get("qty")

        return serialized_data

    except Exception as e:
        raise WildberriesError(e)
