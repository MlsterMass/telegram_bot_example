from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.language_packs_middleware import _

quantity_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("I'm agree"), callback_data="agree")
        ],
        [
            InlineKeyboardButton(text=_("Change quantity"), callback_data="change")
        ],
        [
            InlineKeyboardButton(text=_("Cancel buying"), callback_data="cancel")
        ]
    ]
)
