from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


post_callback = CallbackData("create_post", "action")
confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
         InlineKeyboardButton(text="Publicate post", callback_data=post_callback.new(action="post")),
         InlineKeyboardButton(text="Decline post", callback_data=post_callback.new(action="cancel"))

        ]
    ]
)

