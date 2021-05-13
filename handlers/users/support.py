from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.inline.support import support_keyboard, support_callback
from loader import dp, bot


@dp.message_handler(Command("support"))
async def ask_support(message: types.Message):
    text = "<b>Do you want to send message to support?</b><i> Click button below</i>"
    keyboard = await support_keyboard(messages="one")
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="one"))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    user_id = int(callback_data.get("user_id"))

    await call.message.answer("<b>Send here your message to support</b>")
    await state.set_state("wait_for_support_message")
    await state.update_data(second_id=user_id)


@dp.message_handler(state="wait_for_support_message", content_types=types.ContentType.ANY)
async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data["second_id"]

    await bot.send_message(second_id,
                           f"<b>You got message!</b><i> Click on button below</i>")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
    await message.send_copy(second_id, reply_markup=keyboard)
    await message.answer("<b>You send message</b>")
    await state.reset_state()