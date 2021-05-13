from random import random

from aiogram import types
from aiogram.dispatcher.filters import Command

from data.items import BTC, ETH, POST_REGULAR_SHIPPING, POST_EXTRA_SHIPPING, PICKUP_SHIPPING
from loader import dp, bot


@dp.message_handler(Command("invoices"))
async def send_invoices(message: types.Message):
    await bot.send_invoice(message.from_user.id,
                           **BTC.generate_item(),
                           payload="123456")

    await bot.send_invoice(message.from_user.id,
                           **ETH.generate_item(),
                           payload="123457")


@dp.shipping_query_handler()
async def choose_delivery(query: types.ShippingQuery):
    if query.shipping_address.country_code == "UA":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[
                                            POST_REGULAR_SHIPPING,
                                            POST_EXTRA_SHIPPING,
                                            PICKUP_SHIPPING
                                        ],
                                        ok=True)
    elif query.shipping_address.country_code == "US":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="We don't delivery in this country")
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[
                                            POST_REGULAR_SHIPPING
                                        ],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id,
                                        ok=True)
    await bot.send_message(chat_id=query.from_user.id, text="Thank you for your purchase!\n"
                                                            " We will deliver your goods as soon as possible")
