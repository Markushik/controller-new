from aiogram.fsm.state import StatesGroup, State


class UserSG(StatesGroup):
    MAIN = State()
    SUBS = State()
    HELP = State()
    DONATE = State()


class SubscriptionSG(StatesGroup):
    SERVICE = State()
    MONTHS = State()
    REMINDER = State()
    CHECK = State()
