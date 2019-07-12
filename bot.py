import logging
import config

from handler import five_am_handler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=[ContentType.PHOTO])
async def image_handler(message: types.Message):
    _from = message["from"]
    _date = message.date
    _chat = message.chat
    reply = five_am_handler(chat=_chat, user=_from, time=_date)
    await message.reply(reply)


async def download_image(message: types.Message):
    raw = message.photo[2].file_id
    file_info = await bot.get_file(raw)
    photo = await bot.download_file(file_info.file_path)
    await bot.send_photo(message.chat.id, photo, caption='Nice pic!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
