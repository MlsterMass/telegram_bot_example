from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
# from loader import db
from utils.db_api import db_gino
from utils.db_api.db_gino import db


async def on_startup(dispatcher):
    # Уведомляет про запуск
    print("Connect BD")
    await db_gino.on_startup(dp)
    # print("Clean BD")
    # await db.gino.drop_all()

    await set_default_commands(dp)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
