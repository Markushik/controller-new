from aiogram_dialog import DialogManager, StartMode
from loguru import logger

from src.presentation.tgbot.states.user import MainMenu


async def on_unknown_intent(event, dialog_manager: DialogManager):
    logger.error('Restarting dialog: %s', event.exception)
    await dialog_manager.start(state=MainMenu.MAIN, mode=StartMode.RESET_STACK)


async def on_unknown_state(event, dialog_manager: DialogManager):
    logger.error('Restarting dialog: %s', event.exception)
    await dialog_manager.start(state=MainMenu.MAIN, mode=StartMode.RESET_STACK)
