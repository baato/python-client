import pytest
import requests
from baato.config import __baato_endpoint__
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN


def test_endpoint():
    res = requests.get(__baato_endpoint__)
    assert res.status_code == 401


def test_client_without_token():
    with pytest.raises(Exception):
        BaatoClient()


def test_client_endpoint():
    client = BaatoClient(access_token=BAATO_ACCESS_TOKEN)
    assert client.endpoint == "https://api.baato.io/api"


def test_client_version():
    client = BaatoClient(access_token=BAATO_ACCESS_TOKEN)
    assert client.version == "v1"


def test_client_custom_url():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN, endpoint="http://baato.io")
    assert res.endpoint == "http://baato.io"


def test_client_custom_url_exception():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN, endpoint="test")


def test_client_token_invalid_token():
    res = BaatoClient(access_token="TEST").search(q="kathmandu")
    assert res["status"] == 403
