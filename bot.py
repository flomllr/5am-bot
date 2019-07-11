# Imports
import os
import logging

from os.path import join, dirname
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

# .env config
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_TOKEN = os.getenv('TOKEN')

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
