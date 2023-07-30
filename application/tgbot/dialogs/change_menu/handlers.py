from aiogram.methods import SendMessage
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.states import ChangeMenu


async def on_click_sub_change(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        item_id: str
) -> None:
    await dialog_manager.start(ChangeMenu.PARAMETERS, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data["service_id"] = int(item_id)


async def on_click_get_change_menu(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(ChangeMenu.CHANGE, mode=StartMode.RESET_STACK)


async def on_click_change_title(
        query: CallbackQuery,
        dialog: DialogProtocol,
        dialog_manager: DialogManager
) -> SendMessage:
    await dialog_manager.start(ChangeMenu.TITLE, mode=StartMode.RESET_STACK)


async def on_click_change_months(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(ChangeMenu.MONTHS, mode=StartMode.RESET_STACK)


async def on_click_change_date(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(ChangeMenu.REMINDER, mode=StartMode.RESET_STACK)
