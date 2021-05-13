import sqlite3
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import CallbackQuery

from keyboards.inline.start_choose_lang import languages_markup
from loader import dp, bot
from utils.db_api import db_commands as commands

from middlewares.language_packs_middleware import _


# from filters import IsPrivate


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    global user
    chat_id = message.from_user.id
    referral = message.get_args()
    try:
        user = await commands.add_new_user(id=chat_id, referral=referral)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    id = user.user_id
    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={id}"
    count_users = await commands.count_users()
    text = _("Welcome\n"
             "Now in base {count_users} users\n"
             "Your referral link: {bot_link}"
             "Check referrals command /referrals\n"
             "Items list: /items").format(count_users=count_users, bot_link=bot_link)
    await message.answer(text, reply_markup=languages_markup)


@dp.callback_query_handler(text_contains="lang")
async def choose_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    lang = call.data[-2:]
    await commands.set_language(language=lang)
    await call.message.answer(_("Your language was changed.", locale=lang))


@dp.message_handler(Command("referrals"))
async def check_referrals(message: types.Message):
    referrals = await commands.check_referrals()
    text = _("Your referrals: {referrals}").format(referrals=referrals)
    await message.answer(text)
