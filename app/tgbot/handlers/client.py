from datetime import date, datetime

import asyncstdlib
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, DialogProtocol
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Services, Users
from app.tgbot.dialogs.format import I18N_FORMAT_KEY
from app.tgbot.states.user import SubscriptionSG, UserSG

router = Router()


@router.message(CommandStart(), StateFilter("*"))
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Users(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            chat_id=message.chat.id,
            count_subs=0,
        )
    )
    await session.commit()

    await dialog_manager.start(UserSG.MAIN, mode=StartMode.RESET_STACK)


async def on_click_get_subs_menu(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_back_to_main_menu(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.MAIN, mode=StartMode.RESET_STACK)


async def on_click_get_settings_menu(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.SETTINGS, mode=StartMode.RESET_STACK)


async def on_click_get_help_menu(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.HELP, mode=StartMode.RESET_STACK)


async def on_click_get_delete_menu(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


async def get_subs_for_output(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    request = await session.execute(
        select(Services)
        .where(Services.service_by_user_id == dialog_manager.event.from_user.id)
    )
    result_all = request.all()
    subs = [
        f"<b>{count + 1}. {item.Services.title}</b> — {datetime.date(item.Services.reminder)}\n"
        async for count, item in asyncstdlib.enumerate(result_all)
    ]

    match result_all:
        case []:
            return {
                "subs": "<b>🤷‍♂️ Кажется</b>, мы ничего <b>не нашли...</b>"
            }
        case _:
            return {
                "subs": ''.join(subs)
            }


async def get_subs_for_delete(dialog_manager: DialogManager, **kwargs) -> dict[str, str | list[tuple[str, str, str]]]:
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


async def on_click_start_create_sub(query: CallbackQuery, dialog: DialogProtocol,
                                    dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    request = await session.execute(
        select(Users)
        .where(Users.user_id == dialog_manager.event.from_user.id)
    )
    result_all = request.one()

    if int(result_all.Users.count_subs) <= 7:
        await dialog_manager.start(SubscriptionSG.SERVICE, mode=StartMode.RESET_STACK)
    else:
        await query.message.edit_text("<b>🚫 Ошибка:</b> Достигнут лимит подписок")
        await dialog_manager.done()
        await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


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


async def on_click_calendar_reminder(query: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                     selected_date: date) -> None:
    dialog_manager.dialog_data["reminder"] = selected_date.isoformat()
    await dialog_manager.switch_to(SubscriptionSG.CHECK)


async def on_click_button_confirm(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Services(
            title=dialog_manager.dialog_data.get('service'),
            months=dialog_manager.dialog_data.get('months'),
            reminder=datetime.fromisoformat(dialog_manager.dialog_data.get('reminder')),
            service_by_user_id=query.from_user.id
        )
    )
    await session.merge(
        Users(
            user_id=query.from_user.id,
            count_subs=Users.count_subs + 1
        )
    )
    await session.commit()

    await query.message.edit_text("<b>✅ Одобрено:</b> Данные успешно записаны")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def on_click_button_reject(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await query.message.edit_text("<b>❎ Отклонено:</b> Данные не записаны")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.SUBS, mode=StartMode.RESET_STACK)


async def get_input_service_data(dialog_manager: DialogManager, **kwargs) -> dict[str, str, str]:
    return {
        "service": f"<b>Сервис:</b> <code>{dialog_manager.dialog_data.get('service')}</code>\n",
        "months": f"<b>Длительность:</b> <code>{dialog_manager.dialog_data.get('months')} (мес.)</code>\n",
        "reminder": f"<b>Оповестить: </b> <code>{dialog_manager.dialog_data.get('reminder')}</code>"
    }


async def on_click_sub_selected(query: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                item_id: str) -> None:
    await dialog_manager.start(UserSG.CHECK_DELETE, mode=StartMode.RESET_STACK)
    dialog_manager.dialog_data["service_id"] = int(item_id)


async def on_click_sub_delete(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.execute(
        delete(Services)
        .where(Services.service_id == dialog_manager.dialog_data.get('service_id'))
    )
    await session.merge(
        Users(
            user_id=query.from_user.id,
            count_subs=Users.count_subs - 1
        )
    )
    await session.commit()

    await query.message.edit_text("<b>✅ Одобрено:</b> Подписка успешно удалена")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


async def on_click_sub_not_delete(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    await query.message.edit_text("<b>❎ Отклонено:</b> Подписка не удалена")
    await dialog_manager.done()
    await dialog_manager.start(UserSG.DELETE, mode=StartMode.RESET_STACK)


async def on_click_change_lang_to_ru(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns = dialog_manager.middleware_data["l10ns"]
    lang = "ru"
    l10n = l10ns[lang]
    dialog_manager.middleware_data[I18N_FORMAT_KEY] = l10n.format_value

    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Users(
            user_id=query.from_user.id,
            language="ru"
        )
    )
    await session.commit()

    await query.answer("Вы сменили язык на 🇷🇺 Русский")


async def on_click_change_lang_to_en(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    l10ns = dialog_manager.middleware_data["l10ns"]
    lang = "en"
    l10n = l10ns[lang]
    dialog_manager.middleware_data[I18N_FORMAT_KEY] = l10n.format_value

    session: AsyncSession = dialog_manager.middleware_data["session"]
    await session.merge(
        Users(
            user_id=query.from_user.id,
            language="en"
        )
    )
    await session.commit()

    await query.answer("You switched language to 🇬🇧 English")
