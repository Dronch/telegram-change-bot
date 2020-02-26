# -*- coding: utf-8 -*-

WEB_EXTRACTOR_SOURCE = 'invalid'
WEB_EXTRACTOR_TIMEOUT = 5

DATABASE_SQLALCHEMY_URL = 'sqlite:///app.db'

CACHE_TIMEOUT = 60 * 10

BASE_CURRENCY = 'USD'

TELEGRAM_REQUEST_KWARGS = {
    'proxy_url': 'socks5://localhost:9050'
}
