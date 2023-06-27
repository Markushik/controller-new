from datetime import date, datetime

import asyncstdlib
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import select, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Services, Users
from app.tgbot.dialogs.format import I18N_FORMAT_KEY
from app.tgbot.states.user import SubscriptionSG, UserSG

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
            chat_id=message.chat.id, count_subs=0,
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


async def get_subs_for_output(dialog_manager: DialogManager, **kwargs) -> dict[
    str, str]:  # FIXME: DON'T USE THIS! I will rewrite soon
    """
    The get_subs_for_output function is used to get all the subscriptions for a user.
    It returns a dictionary with one key, which contains the text of all the subscriptions.

    :param dialog_manager: DialogManager: Access the dialog manager
    :return: A dictionary with the subs key and a string value
    """
    session: AsyncSession = dialog_manager.middleware_data["session"]
    request: Result = await session.execute(
        select(Services)
        .where(Services.service_by_user_id == dialog_manager.event.from_user.id)
    )
    result_all = request.scalars().all()

    request1 = await session.execute(
        select(Users)
        .where(Users.user_id == dialog_manager.event.from_user.id)
    )
    result_all2 = request1.scalars().one()
    print(result_all2.language)

    subs = [f"<b>{count + 1}. {item.title}</b> — {datetime.date(item.reminder)}\n"
            async for count, item in asyncstdlib.enumerate(result_all)]

    match result_all:
        case []:
            return {
                "subs": "some text"
            }
        case _:
            return {
                "subs": ''.join(subs)
            }


async def get_subs_for_delete(dialog_manager: DialogManager, **kwargs) -> dict[
    str, str | list[tuple[str, str, str]]]:  # FIXME: DON'T USE THIS! I will rewrite soon
    session: AsyncSession = dialog_manager.middleware_data["session"]
    request = await session.execute(
        select(Services)
        .where(Services.service_by_user_id == dialog_manager.event.from_user.id)
    )
    result_all = request.all()
    subs = [
        (item.Services.title, str(item.Services.service_id), str(datetime.date(item.Services.reminder)))
        for item in result_all
    ]

    match result_all:
        case []:
            return {
                "message": "<b>🤷‍♂️ Кажется</b>, здесь <b>нечего удалять</b>...",
                "subs": subs
            }
        case _:
            return {
                "message": "<b>Выберите</b> подписку, которую <b>хотите удалить</b>:",
                "subs": subs
            }


async def on_click_start_create_sub(callback: CallbackQuery, dialog: DialogProtocol,
                                    dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    request = await session.execute(
        select(Users)
        .where(Users.user_id == dialog_manager.event.from_user.id)
    )
    result = request.one()

    if result.Users.count_subs >= 7:
        await callback.message.edit_text("<b>🚫 Ошибка:</b> Достигнут лимит подписок")
        await dialog_manager.done()
        await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(SubscriptionSG.SERVICE, mode=StartMode.RESET_STACK)


async def service_name_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    if len(message.text) <= 30:
        dialog_manager.dialog_data["service"] = message.text
        await dialog_manager.switch_to(SubscriptionSG.MONTHS)
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Достигнут лимит символов")


async def months_count_handler(message: Message, dialog: DialogProtocol, dialog_manager: DialogManager) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 12 + 1):
        dialog_manager.dialog_data["months"] = int(message.text)
        await dialog_manager.switch_to(SubscriptionSG.REMINDER)
    else:
        await message.answer(text="<b>🚫 Ошибка:</b> Введены недопустимые символы")


async def on_click_calendar_reminder(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                     selected_date: date) -> None:
    dialog_manager.dialog_data["reminder"] = selected_date.isoformat()
    await dialog_manager.switch_to(SubscriptionSG.CHECK)


async def on_click_button_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Services(
            title=dialog_manager.dialog_data['service'],
            months=dialog_manager.dialog_data['months'],
            reminder=datetime.fromisoformat(dialog_manager.dialog_data['reminder']),
            service_by_user_id=callback.from_user.id
        )
    )
    await session.merge(
        Users(
            user_id=callback.from_user.id,
            count_subs=Users.count_subs + 1
        )
    )
    await session.commit()

    await callback.message.edit_text("<b>✅ Одобрено:</b> Данные успешно записаны")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_button_reject(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await callback.message.edit_text("<b>❎ Отклонено:</b> Данные не записаны")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def get_input_service_data(dialog_manager: DialogManager, **kwargs) -> dict[str, str, str]:
    return {
        "service": dialog_manager.dialog_data.get("service"),
        "months": dialog_manager.dialog_data.get("months"),
        "reminder": dialog_manager.dialog_data.get("reminder")
    }


async def on_click_sub_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                item_id: str) -> None:
    await dialog_manager.start(UserSG.CHECK_DELETE, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data["service_id"] = int(item_id)


async def on_click_sub_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    """
    The on_click_sub_selected function is called when the user clicks on a service in the list of services.
    It starts a new dialog with the UserSG.CHECK_DELETE state group, and sets its mode to StartMode.RESET_STACK,
    which means that the current dialog stack will be cleared before starting this new one.

    :param callback: CallbackQuery: Get information about the user that triggered the callback
    :param button: Button: Get the button object that was clicked
    :param dialog_manager: DialogManager: Access the dialog manager
    :doc-author: Trelent
    """
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.execute(delete(Services).where(Services.service_id == dialog_manager.dialog_data.get('service_id')))
    await session.merge(Users(user_id=callback.from_user.id, count_subs=Users.count_subs - 1))
    await session.commit()

    await callback.message.edit_text("<b>✅ Одобрено:</b> Подписка успешно удалена")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


async def on_click_sub_not_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await callback.message.edit_text("<b>❎ Отклонено:</b> Подписка не удалена")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


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
