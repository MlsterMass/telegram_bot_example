from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink, hcode

from data import config
from data.qiwi_items import items
from keyboards.inline.purchase_buttons import buy_button, paid_button
from loader import dp
from utils.misc.qiwi_payment import Payment, NoPaymentFound, NotEnoughMoney


@dp.message_handler(Command("qiwi_pay"))
async def qiwi_pay(message: types.Message):
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
                price=item.price
            ),
            reply_markup=buy_button(item_id=item.id)
        )


@dp.callback_query_handler(text_contains="buy")
async def create_invoice_qiwi(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(':')[-1]
    item_id = int(item_id) - 1
    item = items[item_id]
    amount = item.price

    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        "\n".join(
            [
                f"Pay {amount:.2f} by phone number or address",
                "",
                hlink(config.QIWI_WALLET, url=payment.invoice),
                "Your payment ID",
                hcode(payment.id)
            ]
        ),
        reply_markup=paid_button
    )
    await state.set_state("q_pay")
    await state.update_data(payment=payment)


@dp.callback_query_handler(text="decline", state="q_pay")
async def decline_payment(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Declined payment")
    await state.finish()


@dp.callback_query_handler(text="paid", state="q_pay")
async def approve_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment = data.get("payment")
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer("Payment not found")
        return
    except NotEnoughMoney:
        await call.message.answer("Not enough money")
        return
    else:
        await call.message.answer("Purchase paid")
    await call.message.delete_reply_markup()
    await state.finish()
