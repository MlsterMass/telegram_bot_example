from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.confirm_create_item_admin_panel import item_confirm
from keyboards.inline.mailing_admin_buttons import mailing_buttons

from loader import dp, bot
from middlewares.language_packs_middleware import _
from states.mailing import Mailing
from states.new_item import NewItem
from utils.db_api.schemas.user import User
from utils.db_api.schemas.items import Item


@dp.message_handler(Command("cancel"), user_id=ADMINS, state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(_("You decline creating of item"))
    await state.reset_state()


@dp.message_handler(Command("add_item"), user_id=ADMINS)
async def add_item(message: types.Message):
    await message.answer(_("Input item name or click /cancel"))
    await NewItem.Name.set()


@dp.message_handler(user_id=ADMINS, state=NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer(_("Name of product: {name}\n"
                           "Send me photo of product(no document) or click /cancel").format(
        name=name
    )
    )
    await NewItem.Photo.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=ADMINS, state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item = data.get("item")
    item.photo = photo
    await message.answer_photo(
        photo=photo,
        caption=_("Product name: {name}"
                  "\nSend me product price in coins or click /cancel").format(name=item.name)
    )
    await NewItem.Price.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=ADMINS, state=NewItem.Price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer(_("Incorrect value, input for example: 100000"))
        return
    item.price = price
    await message.answer(_("Price:{price:.2f}\n"
                           "Confirm ? Click /cancel for decline operation").format(price=item.price),
                         reply_markup=item_confirm)
    await state.update_data(item=item)
    await NewItem.Confirm.set()


@dp.callback_query_handler(text="change", user_id=ADMINS,
                           state=NewItem.Confirm)
async def change_price(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("If you want to change price\n"
                                "Input price in coins format"))
    await NewItem.Price.set()


@dp.callback_query_handler(text="confirm", user_id=ADMINS,
                           state=NewItem.Confirm)
async def confirm_price(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item = data.get("item")
    await item.create()
    await call.message.answer(_("Item was created"))
    await state.finish()


@dp.message_handler(Command("tell_all"), user_id=ADMINS)
async def mailing(message: types.Message):
    await message.answer(_("Send text of mailing"))
    await Mailing.Text.set()


@dp.message_handler(user_id=ADMINS, state=Mailing.Text)
async def enter_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(_("In what language you do you want to send mailing?\n"
                           "Text:\n"
                           "{text}").format(text=text),
                         reply_markup=mailing_buttons)
    await Mailing.Language.set()


@dp.callback_query_handler(user_id=ADMINS, state=Mailing.Language)
async def choose_language(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    await state.reset_state()
    await call.message.edit_reply_markup()
    users = await User.query.where(User.language == call.data).gino.all()
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.3)
        except Exception:
            pass
    await call.message.answer(_("Mailing successfully  ended"))
