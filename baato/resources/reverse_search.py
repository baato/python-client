import requests
from ..exceptions import InvalidParams
import logging

logger = logging.getLogger("__name__")


def baato_reverse_search(*args, **kwargs):
    baato_url = kwargs.pop("baseURL")
    access_key = kwargs.pop("access_token")
    if any(qparm not in kwargs for qparm in ("lat", "lon")):
        raise InvalidParams("lat, lon parameter must be provide for search request")
    try:
        params = ""
        for param_name, value in kwargs.items():
            params += f"{param_name}={value}&"
        res = requests.get(f"{baato_url}reverse?key={access_key}&{params}")
        return res
    except requests.exceptions.RequestException as err:
        logger.debug(f"Exception occure in reverse API {err}")
