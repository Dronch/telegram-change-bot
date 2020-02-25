from ..core import ExchangeRateExtractor, ExchangeRate, ExchangeRateError
from typing import List
from types import ModuleType

import requests
import json
import datetime as dt


class ExchangeratesapiIoExtractor(ExchangeRateExtractor):

    name = "exchangeratesapi.io"

    def init(self, config: ModuleType):
        self.timeout = getattr(config, 'WEB_EXTRACTOR_TIMEOUT', 5)

    def list(self, from_currency: str) -> List[ExchangeRate]:
        try:
            response = requests.get(
                f'https://api.exchangeratesapi.io/latest?base={from_currency}',
                timeout=self.timeout
            )
            data = response.json()
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
        except requests.exceptions.ReadTimeout:
            raise ExchangeRateError(
                f"Can't access exchangeratesapi.io - Timeout reached ({self.timeout} seconds)."
            )
        except json.decoder.JSONDecodeError:
            raise ExchangeRateError(
                f"Can't access exchangeratesapi.io - invalid response structure."
            )

    def history(self, from_currency: str, to_currency: str) -> List[ExchangeRate]:
        pass
