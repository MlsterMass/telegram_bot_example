from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from data.config import I18N_DOMAIN, LOCALES_DIR
from loader import dp
from utils.db_api import db_commands


async def get_lang(user_id):
    user = await db_commands.select_user(user_id)
    if user:
        return user.language


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n


i18n = setup_middleware(dp)

_ = i18n.gettext
