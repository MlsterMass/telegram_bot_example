from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import contact_buttons
from loader import dp


@dp.message_handler(Command("callback"))
async def get_contact(message: types.Message):
    await message.answer(f"Hello, {message.from_user.get_mention(as_html=True)}\n"
                         f"Our manager call you\n"
                         f"Click on button below!",
                         reply_markup=contact_buttons.keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def catch_contact(message: types.Message):
    contact = message.contact
    await message.answer(f"Thank you, <b><i>{contact.full_name}</i></b>\n"
                         f"Your number <b>{contact.phone_number}</b> get and resent to manager, waiting...",
                         reply_markup=ReplyKeyboardRemove())
