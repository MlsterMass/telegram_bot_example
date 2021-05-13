from aiogram.dispatcher.filters.state import StatesGroup, State


class Purchase(StatesGroup):
    EnterQuantity = State()
    Approval = State()
    Payment = State()
