from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    MAIN = State()
    CONTROL = State()
    SETTINGS = State()
    HELP = State()


class CreateMenu(StatesGroup):
    TITLE = State()
    MONTHS = State()
    REMINDER = State()
    CHECK_ADD = State()


class ChangeMenu(StatesGroup):
    CHANGE = State()
    PARAMETERS = State()
    TITLE = State()
    MONTHS = State()
    REMINDER = State()
    CHECK_CHANGE = State()


class DeleteMenu(StatesGroup):
    DELETE = State()
    CHECK_DELETE = State()
