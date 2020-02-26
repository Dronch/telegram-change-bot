# -*- coding: utf-8 -*-
import pytest
import requests_mock
import requests
import json
import datetime as dt


from telegram_change_bot.exchange_rate.core import ExchangeRateExtractor, ExchangeRateError, ExchangeRate
from telegram_change_bot.exchange_rate.exchange_rate_implementations.exchangeratesapi_io import (
    ExchangeratesapiIoExtractor
)

from tests import valid_config


@pytest.fixture
def extractor():
    yield ExchangeRateExtractor.from_config(valid_config)


def test_valid_config():
    extractor = ExchangeRateExtractor.from_config(valid_config)
    assert isinstance(extractor, ExchangeratesapiIoExtractor)


def test_list(extractor):
    with requests_mock.Mocker() as mock:
        mock.get(
            'https://api.exchangeratesapi.io/latest?base=USD',
            text=json.dumps({
                "rates": {
                    "CAD": 1.3286900369,
                    "HKD": 7.7901291513,
                    "ISK": 128.5055350554
                },
                "base": "USD",
                "date": "2020-02-25"
            })
        )
        items = extractor.list('USD')

        assert isinstance(items, list)
        for item in items:
            assert isinstance(item, ExchangeRate)


def test_list_timeout(extractor):
    with requests_mock.Mocker() as mock:
        mock.get('https://api.exchangeratesapi.io/latest?base=USD', exc=requests.exceptions.ReadTimeout)
        with pytest.raises(ExchangeRateError):
            extractor.list('USD')


def test_list_invalid_response(extractor):
    with requests_mock.Mocker() as mock:
        mock.get('https://api.exchangeratesapi.io/latest?base=USD', text='invalid')
        with pytest.raises(ExchangeRateError):
            extractor.list('USD')


def test_list_error(extractor):
    with requests_mock.Mocker() as mock:
        mock.get('https://api.exchangeratesapi.io/latest?base=USD', text=json.dumps({"error": ":("}))
        with pytest.raises(ExchangeRateError):
            extractor.list('USD')


def test_history(extractor):
    with requests_mock.Mocker() as mock:
        mock.get(
            'https://api.exchangeratesapi.io/history?start_at=2019-11-27&end_at=2019-12-03&base=USD&symbols=CAD',
            text=json.dumps({
                "rates": {
                  "2019-11-27": {
                    "CAD": 1.3266418385
                  },
                  "2019-11-28": {
                    "CAD": 1.3289413903
                  },
                  "2019-12-03": {
                    "CAD": 1.3320386596
                  },
                  "2019-12-02": {
                    "CAD": 1.3295835979
                  },
                  "2019-11-29": {
                    "CAD": 1.3307230013
                  }
                },
                "start_at": "2019-11-27",
                "base": "USD",
                "end_at": "2019-12-03"
            })
        )
        items = extractor.history(
            'USD',
            'CAD',
            dt.datetime(year=2019, month=11, day=27).date(),
            dt.datetime(year=2019, month=12, day=3).date()
        )

        assert isinstance(items, list)
        for item in items:
            assert isinstance(item, ExchangeRate)


def test_history_timeout(extractor):
    with requests_mock.Mocker() as mock:
        mock.get(
            'https://api.exchangeratesapi.io/history?start_at=2019-11-27&end_at=2019-12-03&base=USD&symbols=CAD',
            exc=requests.exceptions.ReadTimeout
        )
        with pytest.raises(ExchangeRateError):
            extractor.history(
                'USD',
                'CAD',
                dt.datetime(year=2019, month=11, day=27).date(),
                dt.datetime(year=2019, month=12, day=3).date()
            )


def test_history_invalid_response(extractor):
    with requests_mock.Mocker() as mock:
        mock.get(
            'https://api.exchangeratesapi.io/history?start_at=2019-11-27&end_at=2019-12-03&base=USD&symbols=CAD',
            exc=requests.exceptions.ReadTimeout
        )
        with pytest.raises(ExchangeRateError):
            extractor.history(
                'USD',
                'CAD',
                dt.datetime(year=2019, month=11, day=27).date(),
                dt.datetime(year=2019, month=12, day=3).date()
            )


def test_history_error(extractor):
    with requests_mock.Mocker() as mock:
        mock.get(
            'https://api.exchangeratesapi.io/history?start_at=2019-11-27&end_at=2019-12-03&base=USD&symbols=CAD',
            text=json.dumps({"error": ":("})
        )
        with pytest.raises(ExchangeRateError):
            extractor.history(
                'USD',
                'CAD',
                dt.datetime(year=2019, month=11, day=27).date(),
                dt.datetime(year=2019, month=12, day=3).date()
            )
