from asyncio import sleep
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.utils.callback_data import CallbackData

import states
from data.config import PAYMENT_TOKEN
from keyboards.inline.quantity_purchase_buttons import quantity_buttons
from loader import dp, bot

from utils.db_api import db_commands
from middlewares.language_packs_middleware import _
from utils.db_api.schemas.items import Item
from utils.db_api.schemas.purchase import Purchase

buy_item = CallbackData("buy", "item_id")


@dp.message_handler(Command("buy_items"))
async def show_items(message: types.Message):
    all_items = await db_commands.show_items()
    text = _("<b>Item</b> \t№{id}: <u>{name}</u>\n"
             "<b>Price:</b> \t{price:,}\n")
    for item in all_items:
        buy_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Buy",
                                         callback_data=buy_item.new(item_id=item.id))
                ]
            ]
        )
        await message.answer_photo(
            photo=item.photo,
            caption=text.format(id=item.id, name=item.name,
                                price=item.price / 100),
            reply_markup=buy_button
        )
        await sleep(0.3)


@dp.callback_query_handler(buy_item.filter())
async def buying_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = int(callback_data.get("item_id"))
    await call.message.edit_reply_markup()
    item = await Item.get(item_id)
    if not item:
        await call.message.answer(_("This item not exists"))
        return
    text = _("Do you want to buy this item?\"<b>{name}</b>\" by price {price:,}\n"
             "Input count of items which you want to buy or click /cancel").format(
        name=item.name, price=item.price / 100)
    await call.message.answer(text)
    await states.Purchase.EnterQuantity.set()
    await state.update_data(item=item, purchase=Purchase(
        item_id=item_id,
        purchases=datetime.now(),
        receiver=call.from_user.id
    ))


@dp.message_handler(regexp=r"^(\d+)$", state=states.Purchase.EnterQuantity)
async def enter_quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    async with state.proxy() as data:
        data["purchase"].quantity = quantity
        item = data["item"]
        amount = item.price * quantity
        data["purchase"].amount = amount
        purchase = data["purchase"]

        await message.answer(_("Okey, you want to buy <i>{quantity}</i> {name} by price <b>{price:,}/item</b>\n"
                               "It will be <b>{amount:,}</b>. Accepted?").format(
            quantity=quantity,
            name=item.name,
            amount=amount / 100,
            price=item.price / 100
        ), reply_markup=quantity_buttons)
        await state.update_data(purchase=purchase, item=item)
        await states.Purchase.Approval.set()


@dp.message_handler(state=states.Purchase.EnterQuantity)
async def wrong_quantity(message: types.Message):
    await message.answer(_("Wrong value, input number"))


@dp.callback_query_handler(text_contains="cancel", state=states.Purchase)
async def cancel_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("We cancel this purchase"))
    await state.reset_state()


@dp.callback_query_handler(text_contains="change", state=states.Purchase.Approval)
async def change_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Re-enter the quantity"))
    await states.Purchase.EnterQuantity.set()


@dp.callback_query_handler(text_contains="agree", state=states.Purchase.Approval)
async def change_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    purchase = data.get("purchase")
    item = data.get("item")
    await purchase.create()
    await call.message.answer(
        _("Allright. Pay <b>{amount:,}</b> in one of methods below\n"
          "Click on button to accept").format(
            amount=purchase.amount / 100
        )
    )
    currency = "UAH"
    need_name = True
    need_phone_number = False
    need_email = False
    need_shipping_address = True

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=item.name,
        description=item.name,
        payload=str(purchase.id),
        start_parameter=str(purchase.id),
        currency=currency,
        prices=[
            LabeledPrice(label=item.name,
                         amount=purchase.amount)
        ],
        provider_token=PAYMENT_TOKEN,
        need_email=need_email,
        need_name=need_name,
        need_phone_number=need_phone_number,
        need_shipping_address=need_shipping_address
    )
    await state.update_data(purchase=purchase)
    await states.Purchase.Payment.set()


@dp.pre_checkout_query_handler(state=states.Purchase.Payment)
async def query(query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, ok=True)
    data = await state.get_data()
    purchase: Purchase = data.get('purchase')
    success = await check_payment(purchase)
    if success:
        await purchase.update(
            succefull=True,
            shipping_address=query.order_info.shipping_address.to_python()
            if query.order_info.shipping_address else None,
            phone_number=query.order_info.phone_number,
            receiver=query.order_info.name,
            email=query.order_info.email
        ).appply()
        await state.reset_state()
        await bot.send_message(chat_id=query.from_user.id,
                               text=_("Thank you for purchase!"))
    else:
        await bot.send_message(chat_id=query.from_user.id,
                               text=_("Purchase not complete, try again later"))


async def check_payment(purchase: Purchase):
    return True
