# -*- coding: utf-8 -*-
from types import ModuleType
from functools import wraps

import datetime as dt
import re

from telegram import ChatAction
from telegram.ext import Updater, CommandHandler

from .views import ExchangeRateViews, ExchangeRateError
from .graph import history_graph


def error_handler(f):
    """Decorator for handling internal errors"""
    @wraps(f)
    def decorated(self, bot, update, *args, **kwargs):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        try:
            return f(self, bot, update, *args, **kwargs)
        except ExchangeRateError as e:
            bot.send_message(chat_id=update.message.chat_id, text=str(e))
    return decorated


class Bot:
    """Telegram bot"""

    def __init__(self):
        self.updater = None
        self.dispatcher = None

        self.source = None
        self.base = None

        self.views = None

    def init(self, config: ModuleType):
        """Initialization"""
        self.views = ExchangeRateViews(config)

        token = getattr(config, 'TELEGRAM_TOKEN', None)
        request_kwargs = getattr(config, 'TELEGRAM_REQUEST_KWARGS', {})

        self.source = getattr(config, 'WEB_EXTRACTOR_SOURCE', '3rd parties')
        self.base = getattr(config, 'BASE_CURRENCY', 'USD')

        self.updater = Updater(
            token=token,
            request_kwargs=request_kwargs
        )
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler('start', self.help))
        self.dispatcher.add_handler(CommandHandler('help', self.help))

        self.dispatcher.add_handler(CommandHandler('list', self.list))
        self.dispatcher.add_handler(CommandHandler('exchange', self.exchange, pass_args=True))
        self.dispatcher.add_handler(CommandHandler('history', self.history, pass_args=True))

    def run(self):
        """Run bot"""
        self.updater.start_polling()

    def help(self, bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='\n'.join([
                f'Currency Exchange Bot (based on {self.source})'
                'Commands:',
                f'/list - returns list of all available rates. Base currency - {self.base}',
                f' /exchange 10 {self.base} to CAD - converts to the second currency',
                f'/history {self.base}/CAD for 7 days - image graph chart which shows the exchange rate'
            ])
        )

    @error_handler
    def list(self, bot, update):
        """List all available currencies rates"""
        msg = '\n'.join([str(i) for i in self.views.list()])
        bot.send_message(chat_id=update.message.chat_id, text=msg)

    @error_handler
    def exchange(self, bot, update, args):
        """Calc exchange value"""
        query = ' '.join(args)
        match = re.compile(r'(\d+) %s to ([A-Z]{3})' % self.base).match(query)

        if not match:
            raise ExchangeRateError('Invalid request. Look through /help for more info.')

        value = float(match.group(1))
        to_currency = match.group(2)

        result = self.views.exchange(to_currency, value)

        bot.send_message(chat_id=update.message.chat_id, text=f'{result:.2f} {to_currency}')

    @error_handler
    def history(self, bot, update, args):
        """Get history graph image"""
        query = ' '.join(args)
        match = re.compile(r'%s/([A-Z]{3}) for (\d+) days' % self.base).match(query)

        if not match:
            raise ExchangeRateError('Invalid request. Look through /help for more info.')

        to_currency = match.group(1)
        days = int(match.group(2))

        now = dt.datetime.utcnow()
        ago = now - dt.timedelta(days=days)

        data = self.views.history(to_currency, ago.date(), now.date())
        image = history_graph(data)

        bot.send_photo(update.message.chat_id, photo=image)
