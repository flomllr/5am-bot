# Imports
import os
import logging

from config import CONFIG
from os.path import join, dirname
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

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
async def send_welcome(message: types.Message):
    """
    This handler will be called when cliend sends '/start' or '/help' commands.
    """
    print("Hello world")
    await message.reply("I'm alive.")

# TODO: Make this message handler work
@dp.message_handler(content_types=ContentType.PHOTO)
async def echo(message: types.Message):
    print(message)
    await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
