from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buy_button(item_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Purchase", callback_data=f"buy:{item_id}")
            ]
        ]
    )
    return keyboard


paid_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Paid", callback_data="paid")
        ],
        [
            InlineKeyboardButton(text="Decline", callback_data="decline")
        ]
    ]
)
