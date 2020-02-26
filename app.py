from telegram_change_bot import Bot

import config

import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


bot = Bot()
bot.init(config)
bot.run()
