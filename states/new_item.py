from aiogram.dispatcher.filters.state import StatesGroup, State


class NewItem(StatesGroup):
    Name = State()
    Photo = State()
    Price = State()
    Confirm = State()
    Location = State()
