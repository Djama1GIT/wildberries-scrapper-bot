import requests as requests


class WildberriesError(Exception):
    pass


class WildberriesError404(Exception):
    pass


class WildberriesError500(Exception):
    pass


def get_card_details(article: int | str) -> dict:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    response = requests.get(url)
    data = response.json()

    try:
        products = data.get("data").get("products")
    except:
        raise WildberriesError500(
            f"An unexpected error has occurred while getting card details, "
            f"status_code: {response.status_code}"
        )

    if not products:
        raise WildberriesError404("This article does not exist.")

    return data


def serialize_card_details(card_details: dict) -> dict:
    try:
        data = card_details.get("data")
        product = data.get("products")[0]
        serialized_data = {
            "name": product.get("name"),
            "article": product.get("id"),
            "price": int(product.get("salePriceU")) / 100,
            "rating": product.get("reviewRating"),
            "quantity": 0,
        }

        for size in product.get("sizes"):
            for stock in size.get("stocks"):
                serialized_data["quantity"] += stock.get("qty")

        return serialized_data

    except Exception as e:
        raise WildberriesError(e)
