# from googletrans import Translator
from aiogram import executor, types, Bot, Dispatcher
import logging
from loader import dp

logging.basicConfig(level=logging.INFO)

# translator = Translator()

# @dp.message_handler()
# async def get_data(message: types.Message):
#     translation = translator.translate(message.text, dest='en')
#     translated_text = translation.text
#     await message.reply(translated_text)
import wikipedia

# Echo bot
@dp.message_handler()
async def bot_echo(message: types.Message):
    # print(message.chat.id)
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("Bunday malumot topilmadi")