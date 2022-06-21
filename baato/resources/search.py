import requests
from ..exceptions import InvalidParams
import logging

logger = logging.getLogger("__name__")


def baato_search(*args, **kwargs):
    baato_url = kwargs.pop("baseURL")
    access_key = kwargs.pop("access_token")
    if "q" not in kwargs:
        raise InvalidParams("q parameter must be provide for search request")
    try:
        params = ""
        for k, v in kwargs.items():
            params += f"{k}={v}&"
        res = requests.get(f"{baato_url}search?key={access_key}&{params}")
        return res
    except requests.exceptions.RequestException as err:
        logger.debug(f"Exception occure in search API {err}")
