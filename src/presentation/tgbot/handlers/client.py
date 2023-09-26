from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from src.presentation.tgbot.keyboards.inline import CallbackExtensionBody
from src.presentation.tgbot.states.user import CreateMenu, MainMenu

router = Router()


@router.callback_query(CallbackExtensionBody.filter(F.extension == 'extension'))
async def command_extension(
        callback: CallbackQuery,
        dialog_manager: DialogManager,
        callback_data: CallbackExtensionBody,
) -> None:
    await dialog_manager.done()
    await dialog_manager.start(state=CreateMenu.REMINDER, mode=StartMode.NORMAL)

    dialog_manager.dialog_data['service'] = callback_data.service
    dialog_manager.dialog_data['months'] = callback_data.months

    await callback.answer()


@router.message(CommandStart(), StateFilter('*'))
async def command_start(
        message: Message, dialog_manager: DialogManager
) -> None:
    session = dialog_manager.middleware_data['session']
    user = await session.get_user(user_id=message.from_user.id)

    if user is None:
        await session.add_user(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            chat_id=message.chat.id,
        )
        await session.commit()

    await dialog_manager.start(state=MainMenu.MAIN, mode=StartMode.RESET_STACK)
