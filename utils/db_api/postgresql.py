import asyncio

import asyncpg

from data import config


class Database:
    pool: asyncpg.pool.Pool

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PGUSER,
                password=config.PGPASSWORD,
                host=config.IP
            )
        )

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id INT NO NULL,
        Name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        PRIMARY KEY (id))
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id: int, name: str, email: str = None):
        sql = "INSERT INTO Users (id, name, email) VALUES ($1, $2, $3)"
        try:
            await self.pool.execute(sql, id, name, email)
        except asyncpg.exceptions.UniqueViolationError:
            pass

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Users")

    async def update_user_email(self, email, id):
        sql = "UPDATE Users SET email = $1 WHERE id = $2"
        return await self.pool.execute(sql, email, id)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE True")
