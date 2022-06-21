import pytest
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN

def test_reverse():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN).reverse(lat=27.70446921370009,lon=85.32051086425783)
    assert(res["status"]==200)


def test_reverse_without_query():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).reverse()

def test_reverse_only_lat():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).reverse(lat=27.70446921370009)
    

def test_reverse_only_lon():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).reverse(lon=85.32051086425783)