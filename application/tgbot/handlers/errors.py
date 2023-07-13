from aiogram_dialog import DialogManager, StartMode
from loguru import logger

from application.tgbot.states.user import UserSG


async def on_unknown_intent(event, dialog_manager: DialogManager):
    logger.info("Restarting dialog: %s", event.exception)
    await dialog_manager.start(UserSG.main, mode=StartMode.RESET_STACK)


async def on_unknown_state(event, dialog_manager: DialogManager):
    logger.info("Restarting dialog: %s", event.exception)
    await dialog_manager.start(UserSG.main, mode=StartMode.RESET_STACK)
