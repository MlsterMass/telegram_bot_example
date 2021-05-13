from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.config import channels
from keyboards.inline.check_subscribtion_for_channels import check_button
from loader import dp, bot
from filters.forwarded_message import IsForwarded
from utils.misc import subcription_for_channels


@dp.message_handler(IsForwarded(), content_types=types.ContentType.ANY)
# @dp.message_handler(content_types=types.ContentType.ANY)
async def get_channel_info(message: types.Message):
    await message.answer(f"Message was sent from channel <b>\"{message.forward_from_chat.title}\"</b> \n"
                         f"Username: @{message.forward_from_chat.username}\n"
                         f"ID: {message.forward_from_chat.id}")


@dp.message_handler(IsForwarded(), content_types=types.ContentType.ANY)
# @dp.message_handler(content_types=types.ContentType.ANY)
async def get_group_info(message: types.Message):
    await message.answer(f"Message was sent from group <b>\"{message.chat.title}\"</b> \n"
                         f"Username: @{message.chat.username}\n"
                         f"ID: {message.chat.id}")


@dp.message_handler(Command("channels"))
async def show_channels_list(message: types.Message):
    channels_format = str()
    for channel_id_or_username in channels:
        chat = await bot.get_chat(channel_id_or_username)
        invite_link = await chat.export_invite_link()
        channels_format += f"Channel <a href='{invite_link}'>{chat.title}</a>\n"
    await message.answer(f"You may to subscribe to {channels_format}\n", reply_markup=check_button,
                         disable_web_page_preview=True)


@dp.callback_query_handler(text="check_subs")
async def checker_of_subscription(call: CallbackQuery):
    await call.answer()
    result = str()
    for channel in channels:
        status = await subcription_for_channels.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"Subscription for channel <b>\"{channel.title}\"</b> is subscribed!\n"
        else:
            invite_link = await channel.export_invite_link()
            result += (f"Subscription for channel <b>\"{channel.title}\"</b> is not subscribed!\n"
                       f"<a href='{invite_link}'>Need to subscribe for channel</a>\n")
    await call.message.answer(result, disable_web_page_preview=True)
