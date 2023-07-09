from datetime import datetime, date

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogProtocol, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.states.user import SubscriptionSG, UserSG


async def service_name_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    if len(message.text) <= 30:
        dialog_manager.dialog_data["service"] = message.text
        await dialog_manager.switch_to(SubscriptionSG.months)
    else:
        await message.answer(l10n.format_value("Error-len-limit"))


async def months_count_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    if message.text.isdigit() and int(message.text) in range(1, 12 + 1):
        dialog_manager.dialog_data["months"] = int(message.text)
        await dialog_manager.switch_to(SubscriptionSG.reminder)
    else:
        await message.answer(l10n.format_value("Error-char-limit"))


async def on_click_calendar_reminder(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                     selected_date: date) -> None:
    dialog_manager.dialog_data["reminder"] = selected_date.isoformat()
    await dialog_manager.switch_to(SubscriptionSG.check)


async def on_click_button_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session = dialog_manager.middleware_data["session"]

    await session.add_subscription(
        title=dialog_manager.dialog_data['service'],
        months=dialog_manager.dialog_data['months'],
        reminder=datetime.fromisoformat(dialog_manager.dialog_data['reminder']),
        service_by_user_id=callback.from_user.id
    )
    await session.increment_count(user_id=dialog_manager.event.from_user.id)
    await session.commit()

    await callback.message.edit_text(l10n.format_value("Approve-sub-add"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.subs, mode=StartMode.RESET_STACK)


async def on_click_button_reject(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    await callback.message.edit_text(l10n.format_value("Error-sub-add"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.subs, mode=StartMode.RESET_STACK)
