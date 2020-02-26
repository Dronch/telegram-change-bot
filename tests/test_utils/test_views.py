# -*- coding: utf-8 -*-
import pytest
import datetime as dt


from telegram_change_bot.views import ExchangeRateViews, ExchangeRate, ExchangeRateError

from tests import valid_config


exchange_rate_item = ExchangeRate(
    from_currency='USD',
    to_currency='EUR',
    rate=0.5,
    source='src',
    date=dt.datetime(year=2019, month=11, day=27)
)


@pytest.fixture
def views():
    yield ExchangeRateViews(valid_config)


def test_list(mocker, views):
    views.cache_timeout = 0
    mock = mocker.patch.object(views.extractor, 'list')
    mock.return_value = []
    items = views.list()
    mock.assert_called_once()
    assert isinstance(items, list)
    for item in items:
        assert isinstance(item, ExchangeRate)


def test_list_cache(mocker, views):
    views.cache_timeout = 10 * 60
    mock = mocker.patch.object(views.extractor, 'list')
    mock.return_value = [exchange_rate_item]
    items = views.list()
    mock.assert_not_called()
    assert isinstance(items, list)
    for item in items:
        assert isinstance(item, ExchangeRate)


def test_exchange(mocker, views):
    mock = mocker.patch.object(views, 'list')
    mock.return_value = [exchange_rate_item]
    value = views.exchange('EUR', 10)
    mock.assert_called_once()
    assert value == exchange_rate_item.rate * 10


def test_exchange_error(mocker, views):
    mock = mocker.patch.object(views, 'list')
    mock.return_value = [exchange_rate_item]
    with pytest.raises(ExchangeRateError):
        views.exchange('INV', 10)


def test_history(mocker, views):
    views.cache_timeout = 0
    mock = mocker.patch.object(views.extractor, 'history')
    mock.return_value = []
    items = views.history(
        'CAD',
        dt.datetime(year=2019, month=11, day=27).date(),
        dt.datetime(year=2019, month=12, day=3).date()
    )
    mock.assert_called_once()
    assert isinstance(items, list)
    for item in items:
        assert isinstance(item, ExchangeRate)


def test_history_cache(mocker, views):
    views.cache_timeout = 10 * 60
    mock = mocker.patch.object(views.extractor, 'history')
    mock.return_value = [exchange_rate_item]
    items = views.history(
        'CAD',
        dt.datetime(year=2019, month=11, day=27).date(),
        dt.datetime(year=2019, month=12, day=3).date()
    )
    mock.assert_not_called()
    assert isinstance(items, list)
    for item in items:
        assert isinstance(item, ExchangeRate)
