import requests
from ..exceptions import InvalidParams


def baato_direction(*args, **kwargs):
    baato_url = kwargs.pop("baseURL")
    access_key = kwargs.pop("access_token")
    if any(qparm not in kwargs for qparm in ("points", "mode")):
        raise InvalidParams("points and mode parameters must be provide for search request")

    try:
        points = kwargs.pop("points")
        params = ""
        for param_name, value in kwargs.items():
            params += f"{param_name}={value}&"
        for point in points:
            params += f"points[]={point}&"
        res = requests.get(f"{baato_url}directions?key={access_key}&{params}")
        return res
    except requests.exceptions.RequestException as err:
        print(f"Exception {err}")
