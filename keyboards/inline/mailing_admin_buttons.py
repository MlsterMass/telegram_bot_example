from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mailing_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Russian", callback_data="ru")
        ],
        [
            InlineKeyboardButton(text="English", callback_data="en")
        ],
        [
            InlineKeyboardButton(text="Ukrainian", callback_data="ua")
        ]
    ]
)