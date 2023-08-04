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


class EditMenu(StatesGroup):
    EDIT = State()
    PARAMETERS = State()
    TITLE = State()
    MONTHS = State()
    REMINDER = State()

    CHECK_TITLE_CHANGE = State()
    CHECK_MONTHS_CHANGE = State()
    CHECK_REMINDER_CHANGE = State()


class DeleteMenu(StatesGroup):
    DELETE = State()
    CHECK_DELETE = State()
