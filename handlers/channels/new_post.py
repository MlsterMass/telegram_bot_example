import logging

from aiogram import types


from loader import dp


@dp.channel_post_handler(content_types=types.ContentTypes.ANY)
async def new_post(message: types.Message):
    logging.info(f"New post in channel {message.chat.title}\n"
                 f"{message.text}")
