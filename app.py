# -*- coding: utf-8 -*-
from telegram_change_bot import Bot, config

import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


bot = Bot()
bot.init(config)
bot.run()
