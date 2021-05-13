from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.language_packs_middleware import _

item_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Confirm"), callback_data="confirm"),
            InlineKeyboardButton(text=_("Change"), callback_data="change")

        ]
    ]
)
