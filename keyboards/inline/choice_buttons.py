from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import buy_callback

choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Buy BTC",
            callback_data=buy_callback.new(item_name="btc", quantity=1)
        ),
        InlineKeyboardButton(
            text="Buy ETH",
            callback_data="buy:eth:1"
        ),
        InlineKeyboardButton(
            text="Skip",
            callback_data="skip"
        )
    ]
])

btc_keyboard = InlineKeyboardMarkup()
BTC_LINK = "https://whattomine.com/coins/315-0xbtc-sha3solidity"
btc_link = InlineKeyboardButton(text="Buy BTC", url=BTC_LINK)
btc_keyboard.insert(btc_link)

eth_keyboard = InlineKeyboardMarkup()
ETH_LINK = "https://whattomine.com/coins/315-0xbtc-sha3solidity"
eth_link = InlineKeyboardButton(text="Buy ETH", url=ETH_LINK)
eth_keyboard.insert(eth_link)