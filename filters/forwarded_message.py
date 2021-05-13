from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsForwarded(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.forward_from_chat:
            print("message from channel")
            return message.forward_from_chat.type == types.ChatType.CHANNEL
        elif message.chat:
            print("message from group")
            return message.chat.type == types.ChatType.GROUP
