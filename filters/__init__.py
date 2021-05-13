from loader import dp
from .admin_filter import AdminFilter
from .privat_chat import IsPrivate
# from .group_chat import IsGroup
from .forwarded_message import IsForwarded

if __name__ == "filters":
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(AdminFilter)
    # dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsForwarded)
    pass
