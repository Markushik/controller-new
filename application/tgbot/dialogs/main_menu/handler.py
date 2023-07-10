from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.dialogs.render.format import I18N_FORMAT_KEY
from application.tgbot.states.user import UserSG, SubscriptionSG


async def update_key(dialog_manager: DialogManager, lang: str) -> None:
    l10ns = dialog_manager.middleware_data["l10ns"]
    l10n = l10ns[lang]
    dialog_manager.middleware_data[I18N_FORMAT_KEY] = l10n.format_value


async def on_click_get_subs_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.subs, mode=StartMode.RESET_STACK)


async def on_click_back_to_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.main, mode=StartMode.RESET_STACK)


async def on_click_get_settings_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.settings, mode=StartMode.RESET_STACK)


async def on_click_get_help_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.help, mode=StartMode.RESET_STACK)


async def on_click_get_delete_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.delete, mode=StartMode.RESET_STACK)


async def on_click_sub_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                item_id: str) -> None:
    await dialog_manager.start(UserSG.check_delete, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data["service_id"] = int(item_id)


async def on_click_sub_create(callback: CallbackQuery, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    l10n = dialog_manager.middleware_data["l10n"]
    session = dialog_manager.middleware_data["session"]

    request = await session.get_all_positions(user_id=dialog_manager.event.from_user.id)
    count = request.scalar()

    if count.count_subs >= 7:
        await callback.message.edit_text(l10n.format_value("Error-subs-limit"))
        await dialog_manager.done()
        await dialog_manager.start(UserSG.subs, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(SubscriptionSG.service, mode=StartMode.RESET_STACK)


async def on_click_sub_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10n = dialog_manager.middleware_data["l10n"]
    session = dialog_manager.middleware_data["session"]

    await session.delete_subscription(service_id=dialog_manager.dialog_data['service_id'])
    await session.decrement_count(user_id=dialog_manager.event.from_user.id)
    await session.commit()

    await callback.message.edit_text(l10n.format_value("Approve-sub-delete"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.delete, mode=StartMode.RESET_STACK)


async def on_click_sub_not_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10n = dialog_manager.middleware_data["l10n"]

    await callback.message.edit_text(l10n.format_value("Reject-sub-delete"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.delete, mode=StartMode.RESET_STACK)


async def on_click_change_lang(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        item_id: str
) -> None:
    session = dialog_manager.middleware_data["session"]

    match item_id:
        case "0":
            await callback.answer("Вы сменили язык на 🇷🇺 Русский")
            lang = "ru_RU"
            await session.update_language(user_id=dialog_manager.event.from_user.id, language="ru_RU")
            await session.commit()
        case "1":
            await callback.answer("You switched language to 🇬🇧 English")
            lang = "en_GB"
            await session.update_language(user_id=dialog_manager.event.from_user.id, language="en_GB")
            await session.commit()

    await update_key(dialog_manager, lang)
