import pytest
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN


def test_near_by():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN).near_by(lat=27.70446921370009, lon=85.32051086425783, type="school")
    assert res["status"] == 200


def test_reverse_without_query():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).near_by()


def test_near_by_only_lat():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).near_by(lat=27.70446921370009)


def test_near_by_only_lon():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).near_by(lon=85.32051086425783)


def test_near_by_only_type():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).near_by(type="school")
