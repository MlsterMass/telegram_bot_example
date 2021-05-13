# import io
#
# from aiogram import types
# from aiogram.dispatcher.filters import Command
#
# from filters import AdminFilter, IsGroup
# from loader import dp
#
#
# @dp.message_handler(IsGroup(), Command("set_photo", prefixes="!/"), AdminFilter())
# async def set_new_group_photo(message: types.Message):
#     source_message = message.reply_to_message
#     photo = source_message.photo[-1]
#     photo = await photo.download(destination=io.BytesIO())
#     input_file = types.InputFile(path_or_bytesio=photo)
#     await message.chat.set_photo(photo=input_file)
#
#
# @dp.message_handler(IsGroup(), Command("set_title", prefixes="!/"), AdminFilter())
# async def set_new_group_photo(message: types.Message):
#     source_message = message.reply_to_message
#     title = source_message.text
#     await message.chat.set_title(title)
#
#
# @dp.message_handler(IsGroup(), Command("set_description", prefixes="!/"), AdminFilter())
# async def set_new_group_photo(message: types.Message):
#     source_message = message.reply_to_message
#     description = source_message.text
#     await message.chat.set_description(description)
