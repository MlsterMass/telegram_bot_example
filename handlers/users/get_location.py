from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.default import locations_buttons
from loader import dp
from utils.misc.calc_distance import choose_shortest


@dp.message_handler(Command("get_loc"))
async def get_loc(message: types.Message):
    await message.answer(f"Hello, {message.from_user.get_mention(as_html=True)}\n"
                         f"To show you our nearest marketplaces\n"
                         f"click on button below", reply_markup=locations_buttons.keyboard
                         )


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(message: types.Message):
    location = message.location
    latid = location.latitude
    longtid = location.longitude
    closest_shop = choose_shortest(location)

    text_format = ("Example: <a href='{url}'>{shop_name}</a>\n"
                   "Distance to shop {distance:.1f} km")
    text = "\n\n".join(
        [
            text_format.format(shop_name=shop_name, url=url, distance=distance)
            for shop_name, distance, url, shop_location in closest_shop
        ]
    )
    await message.answer(f"Thank you!\n"
                         f"{text}",
                         disable_web_page_preview=True)

    for shop_name, distance, url, shop_location in closest_shop:
        await message.answer_location(
            latitude=shop_location["lat"],
            longitude=shop_location["lon"]
        )
