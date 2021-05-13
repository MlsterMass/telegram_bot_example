from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Check subscription",
                                 callback_data="check_subs")
        ]
    ]
)
