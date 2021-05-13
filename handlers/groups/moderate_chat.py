# import asyncio
# import datetime
# import re
#
# from aiogram import types
# from aiogram.dispatcher.filters import Command
#
# from filters import IsGroup
# from loader import dp, bot
#
#
# @dp.message_handler(IsGroup(), Command("read_only", prefixes="!/"))
# async def read_only_mode(message: types.Message):
#     member = message.reply_to_message.from_user
#     member_id = message.reply_to_message.from_user.id
#     chat_id = message.chat.id
#     command_parse = re.compile(r"(!read_only|/read_only) ?(\d+)? ?([\w+\D]+)?")
#     parsed = command_parse.match(message.text)
#     time = parsed.group(2)
#     comment = parsed.group(3)
#     if not time:
#         time = 5
#     else:
#         time = int(time)
#     until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
#
#     ReadOnlyPermissions = types.ChatPermissions(
#         can_send_messages=False,
#         can_send_media_messages=False,
#         can_send_other_messages=False,
#         can_send_polls=False,
#         can_add_web_page_previews=False,
#         can_pin_messages=False,
#         can_change_info=False,
#         can_invite_users=True
#     )
#     try:
#         await bot.restrict_chat_member(chat_id, user_id=member_id, permissions=ReadOnlyPermissions,
#                                        until_date=until_date)
#         await message.reply(
#             f"User {member.get_mention(as_html=True)} in read only mode for {time} minutes.Cause {comment}! ")
#     except Exception as err:
#         await message.answer("User is group admin!")
#
#     service_message = await message.reply("This message will delete automatically in 5 seconds")
#     await asyncio.sleep(5)
#     await message.delete()
#     await service_message.delete()
#
#
# @dp.message_handler(IsGroup(), Command("del_read_only", prefixes="!/"))
# async def del_read_only_mode(message: types.Message):
#     member = message.reply_to_message.from_user
#     member_id = message.reply_to_message.from_user.id
#     user_allowed = types.ChatPermissions(
#         can_send_messages=True,
#         can_send_media_messages=True,
#         can_send_other_messages=True,
#         can_send_polls=True,
#         can_add_web_page_previews=True,
#         can_pin_messages=True,
#         can_change_info=False,
#         can_invite_users=True
#     )
#     await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
#     await message.reply(f"User {member.get_mention(as_html=True)} was unblocked!")
#     await asyncio.sleep(5)
#     await message.delete()
#
#
# @dp.message_handler(IsGroup(), Command("ban", prefixes="!/"))
# async def ban_user(message: types.Message):
#     member = message.reply_to_message.from_user
#     member_id = message.reply_to_message.from_user.id
#     await message.chat.kick(user_id=member_id)
#     await message.reply(f"User {member.get_mention(as_html=True)} was banned!")
#
#
# @dp.message_handler(IsGroup(), Command("unban", prefixes="!/"))
# async def ban_user(message: types.Message):
#     member = message.reply_to_message.from_user
#     member_id = message.reply_to_message.from_user.id
#     await message.chat.unban(user_id=member_id)
#     await message.reply(f"User {member.get_mention(as_html=True)} was unbanned!")
