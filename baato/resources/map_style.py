import requests
from ..exceptions import InvalidParams
import logging

logger = logging.getLogger("__name__")


def baato_map_style(*args, **kwargs):
    baato_url = kwargs.pop("baseURL")
    access_key = kwargs.pop("access_token")
    if "style_name" not in kwargs:
        raise InvalidParams("style_name parameter must be provide for search request")

    try:
        style_name = kwargs.pop("style_name")
        res = requests.get(f"{baato_url}styles/{style_name.lower()}?key={access_key}")
        return res
    except requests.exceptions.RequestException as err:
        logger.debug(f"Exception occure in map style API {err}")
