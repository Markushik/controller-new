import markupsafe
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.states import EditMenu, MainMenu


async def on_click_get_edit_menu(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=EditMenu.EDIT, mode=StartMode.RESET_STACK)


async def on_click_set_parameters(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        item_id: int
) -> None:
    await dialog_manager.start(
        state=EditMenu.PARAMETERS,
        mode=StartMode.RESET_STACK,
        data={
            'service_id': item_id
        }
    )


async def on_click_edit_title(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    session = dialog_manager.middleware_data['session']
    item_id = dialog_manager.start_data['service_id']

    service = await session.get_service(service_id=item_id)
    await dialog_manager.start(
        state=EditMenu.TITLE,
        mode=StartMode.RESET_STACK,
        data={
            'service_old': service.title,
            'service_id': item_id
        }
    )


async def edit_service_handler(
        message: Message,
        protocol: DialogProtocol,
        dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']

    if len(message.text) > 30:
        return await message.answer(l10n.format_value('Error-len-limit'))

    dialog_manager.dialog_data['service_id'] = dialog_manager.start_data['service_id']
    dialog_manager.dialog_data['service_old'] = dialog_manager.start_data['service_old']
    dialog_manager.dialog_data['service_new'] = markupsafe.escape(message.text)

    await dialog_manager.switch_to(state=EditMenu.CHECK_TITLE_CHANGE)


async def reject_edit_menu(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    l10n = dialog_manager.middleware_data['l10n']

    await callback.message.edit_text(l10n.format_value('Reject-sub-edit'))
    await dialog_manager.done()
    await dialog_manager.start(state=EditMenu.EDIT, mode=StartMode.RESET_STACK)


async def approve_edit_menu(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    await session.edit_title_subscription(
        service_id=dialog_manager.dialog_data['service_id'],
        title=dialog_manager.dialog_data['service_new']
    )
    await session.commit()  # через get получать и через if проверять, че мёржить в базу

    await callback.message.edit_text(l10n.format_value('Approve-sub-edit'))
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenu.CONTROL, mode=StartMode.RESET_STACK)
