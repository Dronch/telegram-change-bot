# telegram-change-bot

![](https://travis-ci.com/Dronch/telegram-change-bot.svg?branch=master)
![](https://codecov.io/gh/Dronch/telegram-change-bot/branch/master/graph/badge.svg)

## Intro

Telegram change bot is wrapper around 3rd parties sites to get currencies exchange rate. 
Its functionality could be extended by adding any exchange source by implementing new class with existing interface.
This app uses SQLAlchemy orm, so any supported database could be used.

## Environment variables to configurate app

| Variable                | Description                                | Default                 |
| ----------------------- |:------------------------------------------:|------------------------:|
| WEB_EXTRACTOR_SOURCE    | Source name to get exchange rates          | exchangeratesapi.io     |
| WEB_EXTRACTOR_TIMEOUT   | Source reading timeout                     | 5                       |
| DATABASE_SQLALCHEMY_URL | Database connection query                  | sqlite:///app.db        |
| CACHE_TIMEOUT           | Caching timeout in seconds                 | 600                     |
| BASE_CURRENCY           | Base currency we are working with          | USD                     |
| TELEGRAM_PROXY          | Proxy to access telegrame or None          |                         |
| TELEGRAM_TOKEN          | Telegram token                             | !!! REQUIRED !!!        |

## Docker
This example will setup app, mysql and tor (as proxy to access telegram).
Set TELEGRAM_TOKEN in `docker-compose.yml` and run:
```
docker compose up --build
```

## Start locally with SQLite without proxy
```
pipenv install
export TELEGRAM_TOKEN=<your token> 
pipenv run python app.py
```