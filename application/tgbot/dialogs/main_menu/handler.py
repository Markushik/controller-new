from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, DialogProtocol, StartMode
from aiogram_dialog.widgets.kbd import Button

from application.tgbot.dialogs.extras.i18n_format import I18N_FORMAT_KEY
from application.tgbot.states.user import CreateMenu, DeleteMenu, MainMenu


async def on_click_get_subs_menu(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(
        state=MainMenu.CONTROL, mode=StartMode.RESET_STACK
    )


async def on_click_back_to_main_menu(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=MainMenu.MAIN, mode=StartMode.RESET_STACK)


async def on_click_sub_create(
    callback: CallbackQuery,
    protocol: DialogProtocol,
    dialog_manager: DialogManager,
) -> None:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    count_subs = await session.get_user_count_subs(
        user_id=dialog_manager.event.from_user.id
    )

    if count_subs < 7:
        return await dialog_manager.start(state=CreateMenu.TITLE, mode=StartMode.RESET_STACK)

    await callback.message.edit_text(l10n.format_value('error-subs-limit'))
    await dialog_manager.done()
    await dialog_manager.start(state=MainMenu.CONTROL, mode=StartMode.RESET_STACK)


async def on_click_sub_delete(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    l10n = dialog_manager.middleware_data['l10n']
    session = dialog_manager.middleware_data['session']

    await session.delete_subscription(
        service_id=dialog_manager.dialog_data['service_id']
    )
    await session.decrement_count(user_id=dialog_manager.event.from_user.id)
    await session.commit()

    await callback.message.edit_text(l10n.format_value('approve-sub-delete'))
    await dialog_manager.done()
    await dialog_manager.start(
        state=DeleteMenu.DELETE, mode=StartMode.RESET_STACK
    )


async def update_format_key(
    dialog_manager: DialogManager, language: str
) -> None:
    l10n = dialog_manager.middleware_data['l10ns'][language]
    dialog_manager.middleware_data[I18N_FORMAT_KEY] = l10n.format_value


async def on_click_change_lang(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    session = dialog_manager.middleware_data['session']

    language = None

    if item_id == '0':
        language = 'ru_RU'
        await callback.answer('Вы сменили язык на 🇷🇺 Русский')
    if item_id == '1':
        language = 'en_GB'
        await callback.answer('You switched language to 🇬🇧 English')

    await update_format_key(dialog_manager=dialog_manager, language=language)
    await session.update_language(
        user_id=dialog_manager.event.from_user.id, language=language
    )
    await session.commit()
