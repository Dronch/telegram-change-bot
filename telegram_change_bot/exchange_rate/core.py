from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from types import ModuleType

import datetime as dt

from importlib import import_module
from pkgutil import iter_modules
import inspect

from . import exchange_rate_implementations


@dataclass
class ExchangeRate(object):

    from_currency: str
    to_currency: str
    rate: float
    source: str
    date: dt.datetime


class ExchangeRateExtractor(ABC):

    @classmethod
    def from_config(cls, config: ModuleType):
        source = getattr(config, 'WEB_EXTRACTOR_SOURCE', 5)
        for _, sub_path, is_pkg in iter_modules(exchange_rate_implementations.__path__):

            if is_pkg is True:
                continue

            module = import_module(f".{sub_path}", package=exchange_rate_implementations.__name__)

            for obj in vars(module).values():
                if inspect.isclass(obj) and \
                   issubclass(obj, ExchangeRateExtractor) and \
                   getattr(obj, 'name', None) == source:
                    return obj(config)

            raise ValueError(f"There is no implementation for `{source}` source.")

    def __init__(self, config: ModuleType):
        if getattr(self, 'name', None) is None:
            raise ValueError(f"{type(self).__name__} must have a name")
        self.init(config)

    @abstractmethod
    def init(self, config: ModuleType):
        pass

    @abstractmethod
    def list(self, from_currency: str) -> List[ExchangeRate]:
        pass

    @abstractmethod
    def history(self, from_currency: str, to_currency: str) -> List[ExchangeRate]:
        pass


class ExchangeRateError(Exception):
    pass
