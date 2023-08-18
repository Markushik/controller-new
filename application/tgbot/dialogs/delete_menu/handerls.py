from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.user import DeleteMenu


async def on_click_get_delete_menu(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(DeleteMenu.DELETE, mode=StartMode.RESET_STACK)


async def on_click_sub_not_delete(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']

    await callback.message.edit_text(l10n.format_value('Reject-sub-delete'))
    await dialog_manager.done()
    await dialog_manager.start(DeleteMenu.DELETE, mode=StartMode.RESET_STACK)


async def on_click_sub_selected(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: int,
) -> None:
    await dialog_manager.start(
        DeleteMenu.CHECK_DELETE, mode=StartMode.RESET_STACK
    )
    dialog_manager.dialog_data['service_id'] = item_id
