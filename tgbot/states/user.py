from aiogram.fsm.state import StatesGroup, State


class UserSG(StatesGroup):
    service = State()
    months = State()
    check = State()
    reminder = State()
