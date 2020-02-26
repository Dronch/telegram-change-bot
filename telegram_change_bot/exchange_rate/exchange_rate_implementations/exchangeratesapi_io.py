# -*- coding: utf-8 -*-
from ..core import ExchangeRateExtractor, ExchangeRate, ExchangeRateError
from typing import List
from types import ModuleType
from functools import wraps

import requests
import json
import datetime as dt


def remote_exceptions(f):
    """Decorator to handle remote exceptions"""
    @wraps(f)
    def decorated(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except requests.exceptions.ReadTimeout:
            raise ExchangeRateError(
                f"Can't access exchangeratesapi.io - Timeout reached ({self.timeout} seconds)."
            )
        except json.decoder.JSONDecodeError:
            raise ExchangeRateError(
                f"Can't access exchangeratesapi.io - invalid response structure."
            )
    return decorated


class ExchangeratesapiIoExtractor(ExchangeRateExtractor):
    """Exchange rate source, based on exchangeratesapi.io"""

    name = "exchangeratesapi.io"

    def init(self, config: ModuleType):
        self.timeout = getattr(config, 'WEB_EXTRACTOR_TIMEOUT', 5)

    @remote_exceptions
    def list(self, from_currency: str) -> List[ExchangeRate]:
        response = requests.get(
            f'https://api.exchangeratesapi.io/latest?base={from_currency}',
            timeout=self.timeout
        )
        data = response.json()

        if 'error' in data:
            raise ExchangeRateError(data["error"])

        base = data.get('base')
        date = dt.datetime.strptime(data.get('date'), '%Y-%m-%d')
        return [
            ExchangeRate(
                from_currency=base,
                to_currency=currency,
                rate=rate,
                source=self.name,
                date=date
            ) for currency, rate in data.get('rates', {}).items()
        ]

    @remote_exceptions
    def history(
            self, from_currency: str, to_currency: str, start_at: dt.date, end_at: dt.date
    ) -> List[ExchangeRate]:
        response = requests.get(
            f"https://api.exchangeratesapi.io/history?"
            f"start_at={start_at.strftime('%Y-%m-%d')}&"
            f"end_at={end_at.strftime('%Y-%m-%d')}&"
            f"base={from_currency}&"
            f"symbols={to_currency}",
            timeout=self.timeout
        )
        data = response.json()

        if 'error' in data:
            raise ExchangeRateError(data["error"])

        base = data.get('base')
        return [
            ExchangeRate(
                from_currency=base,
                to_currency=currency,
                rate=rate,
                source=self.name,
                date=dt.datetime.strptime(date, '%Y-%m-%d')
            ) for date, exchange_rate in data.get('rates', {}).items() for currency, rate in exchange_rate.items()
        ]
