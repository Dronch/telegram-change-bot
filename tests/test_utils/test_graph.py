# -*- coding: utf-8 -*-
import io
import datetime as dt

from telegram_change_bot.views import ExchangeRate
from telegram_change_bot.graph import history_graph


def test_history_graph():
    image = history_graph([
        ExchangeRate(
            from_currency='USD',
            to_currency='EUR',
            rate=i,
            source='src',
            date=dt.datetime(year=2019, month=11, day=i)
        ) for i in range(1, 10)
    ])
    assert isinstance(image, io.BytesIO)
