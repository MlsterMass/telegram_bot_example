from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from keyboards.inline.support import cancel_support
from loader import dp, bot


class SupportMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)
        state_str = str(await state.get_state())
        if state_str == "in_support":
            data = await state.get_data()
            second_id = data.get("second_id")
            keyboard = await cancel_support(second_id)
            keyboard_second_user = await cancel_support(message.from_user.id)
            await message.send_copy(second_id, reply_markup=keyboard)
            await bot.send_message(second_id, text="", reply_markup=keyboard_second_user)

            raise CancelHandler()
