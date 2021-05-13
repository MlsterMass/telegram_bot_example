from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import allowed_users
from loader import dp


@dp.inline_handler(text="")
async def empty_query(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="111",
                title="Input search query",
                input_message_content=types.InputTextMessageContent(
                    message_text="Don't need click button"
                )
            )
        ],
        cache_time=5
    )


@dp.inline_handler()
async def some_query(query: types.InlineQuery):
    user = query.from_user.id
    if user not in allowed_users:
        await query.answer(
            results=[],
            switch_pm_text="Bot not in use. Connect to bot",
            switch_pm_parameter="connect",
            cache_time=5
        )
        return

    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="1",
                title="Name in inline mode",
                input_message_content=types.InputTextMessageContent(
                    message_text="Some text witch will send on click button"
                ),
                url="https://www.youtube.com/",
                thumb_url="https://i2.wp.com/itc.ua/wp-content/uploads/2020/04/facebook-instagram-youtube-logo"
                          "-clipart-3.jpg?w=1200&quality=100&strip=all&ssl=1",
                description="Description in inline mode"
            ),
            types.InlineQueryResultVideo(
                id="4",
                video_url="https://www.youtube.com/watch?v=hKjAHT4z-PY",
                caption="Scars",
                title="F211 Scars",
                description="Scars clip",
                mime_type="video/mp4",
                thumb_url="https://i2.wp.com/itc.ua/wp-content/uploads/2020/04/facebook-instagram-youtube-logo"
            )
        ]
    )


@dp.message_handler(CommandStart(deep_link="connect"))
async def connect_user(message: types.Message):
    print("test")
    allowed_users.append(message.from_user.id)
    await message.answer("You subscribed",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Start inline mode",
                                                          switch_inline_query_current_chat="Search query")
                                 ]
                             ]
                         ))
