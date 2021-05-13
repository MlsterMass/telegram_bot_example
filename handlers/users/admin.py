from aiogram import types
from filters import IsPrivate
from loader import dp
from data.config import ADMINS


@dp.message_handler(IsPrivate(), text="secret", user_id=ADMINS)
async def admin_chat_secret(message: types.Message):
    await message.answer("Ты админ лови секрет!")
