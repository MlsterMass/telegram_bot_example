from typing import List

from aiogram import types, Bot
from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.db_gino import db
from utils.db_api.schemas.items import Item
from utils.db_api.schemas.menu import Menu
from utils.db_api.schemas.user import User


async def add_user(id: int, name: str, email: str = None):
    try:
        user = User(id=id, name=name, email=email)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_email(id, email):
    user = await User.get(id)
    await user.update(email=email).apply()


async def add_new_user(id: int, referral=None):
    user = types.User.get_current()
    old_user = await select_user(user.id)
    if old_user:
        return old_user
    new_user = User()
    new_user.user_id = user.id
    new_user.username = user.username
    new_user.full_name = user.full_name
    if referral:
        new_user.referral = int(referral)
    await new_user.create()
    return new_user


async def set_language(language):
    user_id = types.User.get_current().id
    user = await select_user(user_id)
    await user.update(language=language).apply()


async def check_referrals():
    bot = Bot.get_current()
    user_id = types.User.get_current().id
    user = await select_user(user_id)
    referrals = await User.query.where(User.referral == user.id).gino.all()
    return " ,".join([
        f"{num + 1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
        for num, referral in enumerate(referrals)
    ])


async def show_items():
    items = await Item.query.gino.all()
    return items


async def add_item(**kwargs):
    newitem = await Menu(**kwargs).create()
    return newitem


async def get_categories() -> List[Menu]:
    return await Menu.query.distinct(Menu.category_code).gino.all()


async def get_subcategories(category) -> List[Menu]:
    return await Menu.query.distinct(Menu.subcategory_code).where(Menu.category_code == category).gino.all()


async def count_items(category_code, subcategory_code=None):
    conditions = [Menu.category_code == category_code]
    if subcategory_code:
        conditions.append(Menu.subcategory_code == subcategory_code)

    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


async def get_items(category_code, subcategory_code) -> List[Menu]:
    items = await Menu.query.where(
        and_(Menu.category_code == category_code,
             Menu.subcategory_code == subcategory_code)
    ).gino.all()
    return items


async def get_item(item_id) -> Menu:
    item = await Menu.query.where(Menu.id == item_id).gino.first()
    return item
