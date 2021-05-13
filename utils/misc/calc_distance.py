import math

from aiogram import types

from utils.misc import show_on_gmaps

from data.locations import Shops

R = 6378.1


def calc_distance(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    print(distance)
    return distance


def choose_shortest(location: types.Location):
    distance = list()
    for shop_name, shop_location in Shops:
        distance.append((shop_name,
                         calc_distance(location.latitude, location.longitude,
                                       shop_location['lat'], shop_location['lon']),
                         show_on_gmaps.show(**shop_location),
                         shop_location))
    return sorted(distance, key=lambda x: x[1])[:2]
