from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.db_api import db_commands as commands


@dp.message_handler(Command("add_email"))
async def add_email(message: types.Message, state: FSMContext):
    await message.answer("Send me your email")
    await state.set_state("email")


@dp.message_handler(state="email")
async def enter_email(message: types.Message, state: FSMContext):
    email = message.text
    await commands.update_user_email(email=email, id=message.from_user.id)
    user = await commands.select_user(id=message.from_user.id)
    await message.answer(f"Data was updated {user.id}, <b>{user.name}</b>, {user.email}")
    await state.finish()
