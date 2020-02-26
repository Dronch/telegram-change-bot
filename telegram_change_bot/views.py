from .database import Database, ExchangeRateModel, Cache
from .exchange_rate import ExchangeRateError, ExchangeRate, ExchangeRateExtractor
from types import ModuleType
from typing import List
from functools import wraps
from dataclasses import asdict

import datetime as dt


def session(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        session = self.db.Session()
        result = f(self, session, *args, **kwargs)
        session.commit()
        session.close()
        return result
    return decorated


def cache(f):
    @wraps(f)
    @session
    def decorated(self, session, *args, **kwargs):
        key = f.__name__ + \
              ' '.join([str(i) for i in args]) + \
              ' '.join(f'{key}: {value}' for key, value in kwargs.items())

        expired = dt.datetime.utcnow() - dt.timedelta(seconds=self.cache_timeout)

        _cache = session.query(Cache).filter_by(key=key).filter(Cache.created_at > expired).first()
        if _cache is None:
            _cache = Cache(key=key)
            session.add(_cache)
            exchange_rates = f(self, *args, **kwargs)
            _cache.exchange_rates = [ExchangeRateModel(**asdict(item)) for item in exchange_rates]
            session.add_all(_cache.exchange_rates)
        else:
            exchange_rates = [
                ExchangeRate(
                    from_currency=item.from_currency,
                    to_currency=item.to_currency,
                    rate=item.rate,
                    source=item.source,
                    date=item.date
                ) for item in _cache.exchange_rates
            ]
        return exchange_rates

    return decorated


class ExchangeRateViews(object):

    def __init__(self, config: ModuleType):
        self.db = Database.from_config(config)
        self.extractor = ExchangeRateExtractor.from_config(config)
        self.cache_timeout = getattr(config, 'CACHE_TIMEOUT', 10 * 60)
        self.base_currency = getattr(config, 'BASE_CURRENCY', 'USD')

    @cache
    def list(self) -> List[ExchangeRate]:
        return self.extractor.list(self.base_currency)

    def exchange(self, to_currency: str, value: float) -> float:
        exchange_rate = next(iter(filter(lambda x: x.to_currency == to_currency, self.list())), None)

        if exchange_rate is None:
            raise ExchangeRateError(f"Can't find target currency: {to_currency}")

        return value * exchange_rate.rate

    @cache
    def history(self, to_currency: str, start_at: dt.date, end_at: dt.date) -> List[ExchangeRate]:
        return self.extractor.history(self.base_currency, to_currency, start_at, end_at)


