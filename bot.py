# Imports
import os
import logging

from config import CONFIG
from os.path import join, dirname
from aiogram import Bot, Dispatcher, executor, types

# config
API_TOKEN = CONFIG['token']

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Methods
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    """
    This handler will be called when cliend sends '/start' or '/help' commands.
    """
    await message.reply("I'm alive.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
