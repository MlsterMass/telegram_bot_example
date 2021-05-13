import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode
from blockcypher import satoshis_to_btc

from data import config
from data.btc_items import items
from keyboards.inline.purchase_buttons import paid_button, buy_button
from loader import dp
from utils.misc.btc_payment import Payment, NotConfirmed, NoPaymentFound
from utils.misc.qr_code_gen import qr_link


@dp.message_handler(Command("btc_pay"))
async def btc_pay(message: types.Message):
    caption = """
    Product : {title}
    <i>Info:</i>
    {description}

    <u>Price:</u> {price:.2f} <b>RUB</b>
    """

    for item in items:
        await message.answer_photo(
            photo=item.photo_link,
            caption=caption.format(
                title=item.title,
                description=item.description,
                price=satoshis_to_btc(item.price)
            ),
            reply_markup=buy_button(item_id=item.id)
        )


@dp.callback_query_handler(text_contains="buy")
async def create_invoice_btc(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(':')[-1]
    item_id = int(item_id) - 1
    item = items[item_id]

    amount = item.price + random.randint(5, 500)
    payment = Payment(amount=amount)
    payment.create()

    show_amount = satoshis_to_btc(payment.amount)
    await call.message.answer(f"Pay this amount: {payment.amount:.8f} on address\n" +
                              hcode(config.WALLET_BTC), reply_markup=paid_button)

    qr_code = config.REQUEST_LINK.format(address=config.WALLET_BTC,
                                         amount=show_amount,
                                         message=f"Purchase{item}"
                                         )
    await call.message.answer_photo(photo=qr_link(qr_code))
    await state.set_state("btc_pay")
    await state.update_data(payment=payment)


@dp.callback_query_handler(text="decline", state="btc_pay")
async def decline_payment(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Declined payment")
    await state.finish()


@dp.callback_query_handler(text="paid", state="btc_pay")
async def approve_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment = data.get("payment")
    try:
        payment.check_payment()
    except NotConfirmed:
        await call.message.answer("Transaction found, but not confirmed")
        return
    except NoPaymentFound:
        await call.message.answer("No transaction found")
        return
    else:
        await call.message.answer("Purchase paid")
    await call.message.delete_reply_markup()
    await state.finish()
