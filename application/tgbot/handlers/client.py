from datetime import date, datetime
from typing import Any

import asyncstdlib
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import select, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.database.models import Services, Users
from application.tgbot.dialogs.format import I18N_FORMAT_KEY
from application.tgbot.states.user import SubscriptionSG, UserSG

router = Router()


@router.message(CommandStart(), StateFilter("*"))
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    """
    The command_start function is called when the user sends a /start command to the bot.
    It creates a new row in the Users table of our database, and then starts a dialog with
    the user using DialogManager.start(). The StartMode parameter tells DialogManager that
    we want to reset any previous dialogs.

    :param message: Message: Access the message data
    :param dialog_manager: DialogManager: Start a new dialog
    """
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Users(
            user_id=message.from_user.id, user_name=message.from_user.first_name,
            chat_id=message.chat.id, count_subs=0,  # FIXME: count cubs == 0, when press "start"
        )
    )
    await session.commit()
    await dialog_manager.start(UserSG.MAIN, mode=StartMode.RESET_STACK)


async def on_click_get_subs_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_get_subs_menu function is a callback function that handles the user's click on the Get Subs button.
    It starts a new dialog with the UserSG.SUBS state group, resetting any previous dialog stack.

    :param callback: CallbackQuery: Get the callback data of the button that was clicked
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Start a new dialog
    """
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_back_to_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_back_to_main_menu function is a callback function that handles the user's
    click on the back to main menu button.
    It resets the dialog stack and starts a new dialog with UserSG.MAIN as its starting state.

    :param callback: CallbackQuery:  Get the callback data of the button that was clicked
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Start a new dialog
    """
    await dialog_manager.start(UserSG.MAIN, mode=StartMode.RESET_STACK)


async def on_click_get_settings_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_get_settings_menu function is a callback function that handles the user's click on the settings button.
    It starts a new dialog with UserSG.SETTINGS as its root state group, and resets the stack of states in this dialog.

    :param callback: CallbackQuery: Get the callback data of the button that was clicked
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Start a new dialog
    """
    await dialog_manager.start(UserSG.SETTINGS, mode=StartMode.RESET_STACK)


async def on_click_get_help_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_get_help_menu function is a callback function that handles the user's click on the help button.
    It starts a new dialog with the UserSG.HELP state graph, resetting any previous dialogs.

    :param callback: CallbackQuery: Get the callback data of the button that was clicked
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Start a new dialog
    """
    await dialog_manager.start(UserSG.HELP, mode=StartMode.RESET_STACK)


async def on_click_get_delete_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_get_delete_menu function is a callback function that handles the user's click on the Delete button.
    It starts a new dialog with UserSG.DELETE as its first state, and resets the stack of states in order to avoid any
    conflicts with other dialogs.

    :param callback: CallbackQuery: Get the callback data of the button that was clicked
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Start the dialog
    """
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


async def get_subs_for_output(dialog_manager: DialogManager, **kwargs) -> None:
    """
    The get_subs_for_output function is used to get all the subscriptions for a user.
    It returns a dictionary with one key, which contains the text of all the subscriptions.

    :param dialog_manager: DialogManager: Access the dialog manager
    :return: A dictionary with the subs key and a string value
    """
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session: AsyncSession = dialog_manager.middleware_data["session"]
    request: Result = await session.execute(
        select(Services)
        .where(Services.service_by_user_id == dialog_manager.event.from_user.id)
    )
    services_result = request.scalars().all()

    subs = [f"<b>{count + 1}. {item.title}</b> — {datetime.date(item.reminder)}\n"
            async for count, item in asyncstdlib.enumerate(services_result)]

    match services_result:
        case []:
            return {"subs": l10n.format_value("Nothing-output")}
        case _:
            return {"subs": ''.join(subs)}


# async def get_langs_for_output(dialog_manager: DialogManager, **kwargs) -> None:
#     langs = [" 🇷🇺 Русский", " 🇬🇧 English"]
#
#     return {"langs": langs}


async def get_subs_for_delete(dialog_manager: DialogManager, **kwargs) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session: AsyncSession = dialog_manager.middleware_data["session"]
    request: Result = await session.execute(
        select(Services)
        .where(Services.service_by_user_id == dialog_manager.event.from_user.id)
    )
    services_result = request.fetchall()

    subs = [(item.Services.service_id, item.Services.title, datetime.date(item.Services.reminder).isoformat())
            for item in services_result]

    match services_result:
        case []:
            return {"message": l10n.format_value("Nothing-output"), "subs": subs}
        case _:
            return {"message": l10n.format_value("Set-for-delete"), "subs": subs}


async def on_click_sub_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                item_id: str) -> None:
    await dialog_manager.start(UserSG.CHECK_DELETE, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data["service_id"] = int(item_id)


async def on_click_sub_create(callback: CallbackQuery, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session: AsyncSession = dialog_manager.middleware_data["session"]
    request: Result = await session.execute(select(Users).where(Users.user_id == dialog_manager.event.from_user.id))
    result: Any | None = request.scalar()

    if result.count_subs >= 7:
        await callback.message.edit_text(l10n.format_value("Error-subs-limit"))
        await dialog_manager.done()
        await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(SubscriptionSG.SERVICE, mode=StartMode.RESET_STACK)


async def service_name_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    if len(message.text) <= 30:
        dialog_manager.dialog_data["service"] = message.text
        await dialog_manager.switch_to(SubscriptionSG.MONTHS)
    else:
        await message.answer(l10n.format_value("Error-len-limit"))


async def months_count_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    if message.text.isdigit() and int(message.text) in range(1, 12 + 1):
        dialog_manager.dialog_data["months"] = int(message.text)
        await dialog_manager.switch_to(SubscriptionSG.REMINDER)
    else:
        await message.answer(l10n.format_value("Error-char-limit"))


async def on_click_calendar_reminder(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                     selected_date: date) -> None:
    dialog_manager.dialog_data["reminder"] = selected_date.isoformat()
    await dialog_manager.switch_to(SubscriptionSG.CHECK)


async def on_click_button_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Services(
            title=dialog_manager.dialog_data['service'],
            months=dialog_manager.dialog_data['months'],
            reminder=datetime.fromisoformat(dialog_manager.dialog_data['reminder']),
            service_by_user_id=callback.from_user.id
        )
    )
    await session.merge(Users(user_id=callback.from_user.id, count_subs=Users.count_subs + 1))
    await session.commit()

    await callback.message.edit_text(l10n.format_value("Approve-sub-add"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_button_reject(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    await callback.message.edit_text(l10n.format_value("Error-sub-add"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def get_input_service_data(dialog_manager: DialogManager, **kwargs) -> None:
    return {
        "service": dialog_manager.dialog_data.get("service"),
        "months": dialog_manager.dialog_data.get("months"),
        "reminder": dialog_manager.dialog_data.get("reminder")
    }


async def on_click_sub_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_sub_selected function is called when the user clicks on a service in the list of services.
    It starts a new dialog with the UserSG.CHECK_DELETE state group, and sets its mode to StartMode.RESET_STACK,
    which means that the current dialog stack will be cleared before starting this new one.

    :param callback: CallbackQuery: Get information about the user that triggered the callback
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Access the dialog manager
    """
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.execute(delete(Services).where(Services.service_id == dialog_manager.dialog_data['service_id']))
    await session.merge(Users(user_id=callback.from_user.id, count_subs=Users.count_subs - 1))
    await session.commit()

    await callback.message.edit_text(l10n.format_value("Approve-sub-delete"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


async def on_click_sub_not_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns, lang = dialog_manager.middleware_data["l10ns"], dialog_manager.middleware_data["lang"]
    l10n = l10ns[lang]

    await callback.message.edit_text(l10n.format_value("Reject-sub-delete"))
    await dialog_manager.done()
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


# async def on_click_change_lang(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
#                                item_id: str) -> None:
#     print(item_id)


async def on_click_change_lang_to_ru(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns = dialog_manager.middleware_data["l10ns"]
    lang = "ru"
    l10n = l10ns[lang]
    dialog_manager.middleware_data[I18N_FORMAT_KEY] = l10n.format_value

    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Users(
            user_id=callback.from_user.id,
            language="ru"
        )
    )
    await session.commit()

    await callback.answer("Вы сменили язык на 🇷🇺 Русский")


async def on_click_change_lang_to_en(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns = dialog_manager.middleware_data["l10ns"]
    lang = "en"
    l10n = l10ns[lang]
    dialog_manager.middleware_data[I18N_FORMAT_KEY] = l10n.format_value

    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Users(
            user_id=callback.from_user.id,
            language="en"
        )
    )
    await session.commit()

    await callback.answer("You switched language to 🇬🇧 English")  # TODO: 210-244 - rewrite
