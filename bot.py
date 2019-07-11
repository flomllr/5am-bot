# Imports
import os
import logging

from os.path import join, dirname
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler


# Setup
# .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# Bot
token = os.getenv('TOKEN')
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


# Functions
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


# Command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# Start the bot
updater.start_polling()
