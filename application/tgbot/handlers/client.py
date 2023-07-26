from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from application.tgbot.states.states import MainMenu

router = Router()


@router.message(CommandStart(), StateFilter("*"))
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    session = dialog_manager.middleware_data["session"]
    user = await session.get_user(user_id=message.from_user.id)

    if user is None:
        await session.add_user(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            chat_id=message.chat.id
        )
        await session.commit()

    await dialog_manager.start(MainMenu.MAIN, mode=StartMode.RESET_STACK)
