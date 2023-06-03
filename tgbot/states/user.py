from aiogram.fsm.state import StatesGroup, State


class UserSG(StatesGroup):
    service = State()
    months = State()
    reminder = State()
    check = State()
