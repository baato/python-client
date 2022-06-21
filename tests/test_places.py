import pytest
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN

def test_places():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN).places(place_id=100006)
    assert(res["status"]==200)


def test_places_without_query():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).places()
