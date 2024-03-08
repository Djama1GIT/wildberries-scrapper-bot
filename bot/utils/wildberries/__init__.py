from .apiclient import get_card_details, serialize_card_details


def get_data_about_article(article: int | str) -> dict:
    data = get_card_details(article)
    serialized_data = serialize_card_details(data)

    return serialized_data
