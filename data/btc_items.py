from dataclasses import dataclass


@dataclass
class Item:
    id: int
    title: str
    description: str
    price: float
    photo_link: str


BTC = Item(
    id=1, title="BTC", description="""BTC cryptocurrency""",
    price=0.000000005,
    photo_link="https://bits.media/upload/iblock/9ea/dobytye_v_2010_godu_1_000_btc_vpervye_prishli_v_dvizhenie.jpg"
)

ETH = Item(
    id=2, title="ETH", description="""ETH cryptocurrency""",
    price=0.00000001,
    photo_link="https://bits.media/upload/iblock/9ea/dobytye_v_2010_godu_1_000_btc_vpervye_prishli_v_dvizhenie.jpg"
)

items = [BTC, ETH]
