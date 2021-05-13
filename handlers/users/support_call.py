from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


from keyboards.inline.support import support_keyboard, support_callback, check_support_available, get_support_manager, \
    cancel_support, cancel_support_callback
from loader import dp, bot


@dp.message_handler(Command("support_call"))
async def ask_support_call(message: types.Message):
    text = "<b>Do you want to contact to support?</b><i> Click button below</i>"
    keyboard = await support_keyboard(messages="many")
    if not keyboard:
        await message.answer("All operators are busy now. Try again later.")
        return
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="yes"))
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text("You send ticket to support, waiting for answer")

    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id
    if not support_id:
        await call.message.edit_text("All operators are busy now. Try again later")
        await state.reset_state()
        return
    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(messages="many", user_id=call.from_user.id)

    await bot.send_message(support_id,
                           f"You got message from user {call.from_user.get_mention(as_html=True)}",
                           reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="no"))
async def answer_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(chat=second_id, user=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("Unfortunately the user has already changed his mind")
        return
    await state.set_state("in_support")
    await user_state.set_state("in_support")

    await state.update_data(second_id=second_id)
    keyboard = await cancel_support(second_id)
    keyboard_second_user = await cancel_support(call.from_user.id)

    await call.message.edit_text("You in session with user\n"
                                 "Click button to end session",
                                 reply_markup=keyboard)
    await bot.send_message(second_id,
                           "Support in connection!Send here your message\n"
                           "For decline session click on button below",
                           reply_markup=keyboard_second_user)


@dp.message_handler(state="wait_in_support", content_types=types.ContentTypes.ANY)
async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")
    keyboard = await cancel_support(second_id)
    await message.answer("Wait for operator answer or decline session",
                         reply_markup=keyboard)


@dp.callback_query_handler(cancel_support_callback.filter(), state=["in_support", "wait_in_support", None])
async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)
    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await bot.send_message(user_id, "User cancel session")
    await call.message.edit_text("Session was ended")
    await state.reset_state()
