from aiogram import types

from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import buy_callback
from keyboards.inline.choice_buttons import choice, btc_keyboard, eth_keyboard
from loader import dp, bot


@dp.message_handler(Command("items"))
async def show_items(message: types.Message):
    await message.answer(text="We have for trade - 2 BTC, 10 ETH, 50 ZEC \n"
                              "If you don't wanna buy - click skip button", reply_markup=choice)


@dp.callback_query_handler(buy_callback.filter(item_name="btc"))
async def buying_btc(call: CallbackQuery, callback_data: dict):
    # await bot.answer_callback_query(callback_query_id=call.id)
    await call.answer(cache_time=60)
    # logging.info(f"callback_data = {call.data}")
    # logging.info(f"callback_data dict= {callback_data}")
    quantity = callback_data.get("quantity")
    await call.message.answer(f"You bought {quantity} BTC", reply_markup=btc_keyboard)


@dp.callback_query_handler(buy_callback.filter(item_name="eth"))
async def buying_eth(call: CallbackQuery, callback_data: dict):
    # await bot.answer_callback_query(callback_query_id=call.id)
    await call.answer(cache_time=60)
    # logging.info(f"callback_data = {call.data}")
    # logging.info(f"callback_data dict= {callback_data}")
    quantity = callback_data.get("quantity")
    await call.message.answer(f"You bought {quantity} ETH", reply_markup=eth_keyboard)


@dp.callback_query_handler(text="skip")
async def cancel_buying(call: CallbackQuery):
    # await bot.answer_callback_query(callback_query_id=call.id)
    await call.answer("You cancel purchase", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
