import logging
import config

from handler import five_am_handler, timezone_handler, score_handler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message
from aiogram.types.reply_keyboard import KeyboardButton

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply(
        "Hi! I am 5AM Bot! If you are not in Germany, please contact me privately and send me the /location command!"
    )


@dp.message_handler(content_types=[ContentType.PHOTO])
async def image_handler(message: Message):
    _from = message["from"]
    _date = message.date
    _chat = message.chat
    reply = five_am_handler(chat=_chat, user=_from, time=_date)
    await message.reply(reply)


async def download_image(message: Message):
    raw = message.photo[2].file_id
    file_info = await bot.get_file(raw)
    photo = await bot.download_file(file_info.file_path)
    await bot.send_photo(message.chat.id, photo, caption='Nice pic!')


@dp.message_handler(commands=['location'])
async def get_location(message: Message):
    button = KeyboardButton("Send location", request_location=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]])
    await message.reply(
        text="Please send me your location so I can accurately check your wake-up time.",
        reply_markup=keyboard
    )


@dp.message_handler(commands=['score'])
async def get_score(message: Message):
    date = message.date
    chat = message.chat
    score_handler(chat, date)


@dp.message_handler(content_types=[ContentType.LOCATION])
async def location_handler(message: Message):
    await message.reply(
        text="Thank you!",
        reply_markup=ReplyKeyboardRemove()
    )

    user_id = str(message["from"].id)

    latitude = message.location.latitude
    longitude = message.location.longitude

    timezone_handler(user_id, latitude, longitude)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
