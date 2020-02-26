# -*- coding: utf-8 -*-
import pytest
import datetime as dt

from telegram_change_bot.exchange_rate.core import ExchangeRateExtractor, ExchangeRate

from tests import invalid_config


def test_invalid_config_no_source():
    with pytest.raises(ValueError):
        ExchangeRateExtractor.from_config(invalid_config)


def test_dataclass_print():
    exchange_rate = ExchangeRate('USD', 'EUR', 1.1, 'src', dt.datetime.utcnow())
    assert str(exchange_rate) == 'EUR: 1.10'
