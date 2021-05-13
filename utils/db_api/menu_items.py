import asyncio

from data import config
from utils.db_api.db_commands import add_item
from utils.db_api.db_gino import db


async def add_items():
    await db.set_bind(config.POSTGRES_URL)
    await db.gino.create_all()
    await add_item(name="ASUS",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
                   price=100, photo="442424")
    await add_item(name="DELL",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
                   price=100, photo="442424")
    await add_item(name="Apple",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
                   price=100, photo="442424")
    await add_item(name="Iphone",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="☎️ Телефоны", subcategory_code="Phones",
                   price=100, photo="442424")
    await add_item(name="Xiaomi",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="☎️ Телефоны", subcategory_code="Phones",
                   price=100, photo="442424")
    await add_item(name="PewDiePie",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="📹 На Youtube", subcategory_code="Youtube",
                   price=100, photo="442424")
    await add_item(name="Топлес",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="📹 На Youtube", subcategory_code="Youtube",
                   price=100, photo="442424")
    await add_item(name="Орлёнок",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="🗣 На Вконтакте", subcategory_code="VK",
                   price=100, photo="442424")
    await add_item(name="МДК",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="🗣 На Вконтакте", subcategory_code="VK",
                   price=100, photo="442424")

loop = asyncio.get_event_loop()
loop.run_until_complete(add_items())
