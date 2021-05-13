from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

languages_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Russian", callback_data="lang_ru")
        ],
        [
            InlineKeyboardButton(text="English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton(text="Ukrainian", callback_data="lang_ua")
        ]
    ]
)
