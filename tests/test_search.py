import pytest
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN

def test_search():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN).search(q="kathmandu")
    assert(res["status"]==200)


def test_search_without_query():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).search()