import requests
from ..exceptions import InvalidParams
import logging

logger = logging.getLogger("__name__")


def baato_near_by(*args, **kwargs):
    baato_url = kwargs.pop("baseURL")
    access_key = kwargs.pop("access_token")
    if any(qparm not in kwargs for qparm in ("lat", "lon", "type")):
        raise InvalidParams("type ,lat and lon parameter must be provide for search request")
    try:
        params = ""
        for param_name, value in kwargs.items():
            params += f"{param_name}={value}&"
        res = requests.get(f"{baato_url}search/nearby?key={access_key}&{params}")
        return res
    except requests.exceptions.RequestException as err:
        logger.debug(f"Exception occure in near by API {err}")
