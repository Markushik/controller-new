from aiogram.fsm.state import StatesGroup, State


class UserSG(StatesGroup):
    MAIN = State()
    SUBS = State()
    HELP = State()
    SETTINGS = State()
    DELETE = State()
    CHECK_DELETE = State()


class SubscriptionSG(StatesGroup):
    SERVICE = State()
    MONTHS = State()
    REMINDER = State()
    CHECK = State()
