from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    main = State()
    subs = State()
    help = State()
    settings = State()
    delete = State()
    check_delete = State()


class SubscriptionMenu(StatesGroup):
    service = State()
    months = State()
    reminder = State()
    result = State()
