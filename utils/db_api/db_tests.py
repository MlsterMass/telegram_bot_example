import asyncio

from data import config
from utils.db_api import db_commands
from utils.db_api.db_gino import db


async def test():
    await db.set_bind(config.POSTGRES_URL)
    await db.gino.drop_all()
    await db.gino.create_all()

    await db_commands.add_user(1, "One", "email")
    await db_commands.add_user(2, "Kolya", "kolyan@email")
    await db_commands.add_user(3, "Sanya", "sanya@email")
    await db_commands.add_user(4, "1", "2")
    await db_commands.add_user(5, "John", "doe@email")
    users = await db_commands.select_all_users()
    print(f"After: {users}")

    count_users = await db_commands.count_users()
    print(f"Count: {count_users}")
    user = await db_commands.select_user(id=2)
    print(f"User: {user}")


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
