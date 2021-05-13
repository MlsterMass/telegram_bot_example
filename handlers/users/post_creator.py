from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.config import ADMINS, channels, groups
from keyboards.inline.confirm_keyboard_button import confirm_keyboard, post_callback
from loader import dp, bot
from states.post_creator import NewPost


@dp.message_handler(Command("create_post"))
async def create_post(message: types.Message):
    await message.answer("Send me post for publication")
    await NewPost.EnterMessage.set()


@dp.message_handler(state=NewPost.EnterMessage)
async def enter_message(message: types.Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer("Send your post for check?", reply_markup=confirm_keyboard)
    await NewPost.Confirm.set()


@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("You send post for check!")

    await bot.send_message(chat_id=ADMINS[0], text=f"User {mention} want to make post")
    await bot.send_message(chat_id=ADMINS[0], text=text, parse_mode="HTML", reply_markup=confirm_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post was canceled!")


@dp.message_handler(state=NewPost.Confirm)
async def _post_unknown(message: types.Message):
    await message.answer("Choose publicate post or cancel")


@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post_by_admin(call: CallbackQuery):
    await call.answer("You approve the post", show_alert=True)
    target_channel = channels[0] #делаем пост в канале
    # target_group = groups[0]  #делаем пост в группе
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=ADMINS)
async def decline_post_by_admin(call: CallbackQuery):
    await call.answer("You decline the post", show_alert=True)
    await call.message.edit_reply_markup()
