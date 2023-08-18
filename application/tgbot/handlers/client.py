from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from application.tgbot.states.user import CreateMenu, MainMenu

router = Router()


@router.callback_query(F.data == 'extension_data')
async def command_extension(
        message: Message,
        dialog_manager: DialogManager
) -> None:
    await dialog_manager.done()
    await dialog_manager.start(state=CreateMenu.REMINDER, mode=StartMode.NORMAL)


@router.message(CommandStart(), StateFilter('*'))
async def command_start(
        message: Message,
        dialog_manager: DialogManager
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
