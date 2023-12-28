import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS,CHANNELS
from keyboards.inline.manage_post import confirmation_keyboard,post_callback
from loader import dp,bot
from states.new_post import NewPost

@dp.message_handler(Command("yangi post"))
async def create_post(message: Message):
    await message.answer("Chop etish")
    await NewPost.NewMessage.set()


@dp.message_handler(state=NewPost.NewMessage)
async def enter(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer(f"Postni tekshirish uchun yuboraymi",
                        reply_markup=confirmation_keyboard)
    await NewPost.next()

@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("post yuborildi")
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention} quyidagi post chop etmoqchi")
    await bot.send_message(ADMINS[0], text, parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi")

@dp.message_handler(state=NewPost.Confirm)
async def post(message: Message):
    await message.answer("Chop etish yoki rad etish tanlang")

@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def post(call: CallbackQuery):
    await call.answer("Chop etish ruhsat berildi",show_alert=True)
    target = CHANNELS[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target)

@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=ADMINS)
async def decline(call: CallbackQuery):
    await call.answer("Post rad etildi", show_alert=True)
    await call.message.edit_reply_markup()




