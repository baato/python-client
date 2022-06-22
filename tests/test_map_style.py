import pytest
from baato import BaatoClient
from .utils import BAATO_ACCESS_TOKEN


def test_map_style():
    res = BaatoClient(access_token=BAATO_ACCESS_TOKEN).map_style(style_name="monochrome")
    assert type(res) is dict


def test_map_style_without_query():
    with pytest.raises(Exception):
        BaatoClient(access_token=BAATO_ACCESS_TOKEN).map_style()
