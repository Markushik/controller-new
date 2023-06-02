"""
The main file responsible for launching the bot
"""

import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from loguru import logger

from config import settings
from handlers import client
from tgbot.dialogs.create import dialog
from tgbot.handlers.client import start


async def main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.add("../debug.log", format="{time} {level} {message}", level="DEBUG")
    logger.info("LAUNCHING BOT")

    storage = RedisStorage.from_url(
        url=f"redis://{settings.REDIS_HOST}/{settings.REDIS_DB}",
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    bot = Bot(token=settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=storage)

    setup_dialogs(disp)
    disp.message.register(start, CommandStart())

    disp.include_router(client.router)
    disp.include_router(dialog)

    try:
        await disp.start_polling(bot, allowed_updates=disp.resolve_used_update_types())
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")
