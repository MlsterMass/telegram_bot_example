from aiogram import types
from aiogram.types import LabeledPrice

from utils.item import Item

BTC = Item(
    title="BTC",
    description="Top cryptocurrency in the world",
    currency="UAH",
    prices=[
        LabeledPrice(
            label="BTC",
            amount=1000000
        )
    ],
    start_parameter="buy_btc_invoice",
    photo_url="https://assets.coingecko.com/coins/images/1/small/bitcoin.png?1547033579",
    photo_size=600
)

ETH = Item(
    title="ETH",
    description="Top 2 cryptocurrency in the world",
    currency="UAH",
    prices=[
        LabeledPrice(
            label="ETH",
            amount=100000
        ),
        LabeledPrice(
            label="Discount",
            amount=500
        ),
        LabeledPrice(
            label="Bonus",
            amount=10
        ),
        LabeledPrice(
            label="Delivery",
            amount=5
        )
    ],
    start_parameter="buy_eth_invoice",
    photo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/ETHEREUM-YOUTUBE-PROFILE-PIC.png/150px-ETHEREUM-YOUTUBE-PROFILE-PIC.png",
    photo_size=600,
    need_shipping_address=True,
    is_flexible=True
)

POST_REGULAR_SHIPPING = types.ShippingOption(
    id="reg_post",
    title="Ukr mail",
    prices=[
        LabeledPrice("standard package", 2),
        LabeledPrice("ukr mail delivery", 15),
    ]
)
POST_EXTRA_SHIPPING = types.ShippingOption(
    id="extra_post",
    title="Meest express",
    prices=[
        LabeledPrice("ultra package", 10),
        LabeledPrice("meest delivery", 25),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(
    id="pickup_shipping",
    title="Pickup",
    prices=[
        LabeledPrice("pickup from marketplace", -10)
    ]
)
