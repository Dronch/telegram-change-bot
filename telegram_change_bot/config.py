# -*- coding: utf-8 -*-
from environs import Env

env = Env()
env.read_env()

WEB_EXTRACTOR_SOURCE = env.str('WEB_EXTRACTOR_SOURCE', 'exchangeratesapi.io')
WEB_EXTRACTOR_TIMEOUT = env.int('WEB_EXTRACTOR_TIMEOUT', 5)

DATABASE_SQLALCHEMY_URL = env.str('DATABASE_SQLALCHEMY_URL', 'sqlite:///app.db')

CACHE_TIMEOUT = env.int('CACHE_TIMEOUT', 60 * 10)

BASE_CURRENCY = env.str('BASE_CURRENCY', 'USD')

TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')
TELEGRAM_REQUEST_KWARGS = {
    'proxy_url': env.str('TELEGRAM_PROXY', 'socks5://localhost:9050')
}
