import pytest
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN


def test_direction():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN).direction(
        points=["27.71772,85.32784", "27.73449,85.33714"], mode="car"
    )
    assert res["status"] == 200


def test_direction_without_query():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).direction()


def test_direction_only_points():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).direction(points=["27.71772,85.32784", "27.73449,85.33714"])


def test_direction_only_mode():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).direction(mode="car")
