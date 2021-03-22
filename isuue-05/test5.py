import urllib.request
import json
from unittest.mock import patch
import pytest
import test5


def make_request():
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)
    return resp_json


def test_without_patch():
    year = what_is_year_now()
    assert year == 2021


def test_ymd():
    request = {"currentDateTime": "2022-03-22T11:09Z"}
    with patch.object(test5, 'make_request', return_value=request):
        year = what_is_year_now()
    assert year == 2022


def test_dmy():
    request = {"currentDateTime": "01.03.2022_blah_blah"}
    with patch.object(test5, 'make_request', return_value=request):
        year = what_is_year_now()
    assert year == 2022


def test_wrong_format():
    request = {"currentDateTime": "22/03/2022_blah_blah"}
    with patch.object(test5, 'make_request', return_value=request):
        with pytest.raises(ValueError):
            what_is_year_now()


API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """

    resp_json = make_request()

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)

