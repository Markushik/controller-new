# -*- coding: utf-8 -*-
"""
The main file responsible for launching the bot
"""

import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from loguru import logger
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers import client
from tgbot.config import settings
from tgbot.dialogs.create import dialog
from tgbot.dialogs.menu import main_menu
# from tgbot.handlers.errors import dialogs_router
from tgbot.middlewares.database import DbSessionMiddleware


async def main() -> None:  # TODO: add tests with .workflows
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.add(
        "../debug.log", format="{time} {level} {message}", level="DEBUG",
        colorize=True, encoding="utf-8", rotation="5 MB", compression="zip"
    )
    logger.info("LAUNCHING BOT")
    logger.info(settings["REDIS_HOST"])
    storage = RedisStorage.from_url(
        url=f"redis://{settings.REDIS_HOST}/{settings.REDIS_DB}",
        key_builder=DefaultKeyBuilder(with_destiny=True)  # TODO: use dynaconf another
    )
    postgres_url = URL.create(drivername="postgresql+asyncpg", host=settings.POSTGRES_HOST,
                              port=settings.POSTGRES_PORT, username=settings.POSTGRES_USERNAME,
                              password=settings.POSTGRES_PASSWORD, database=settings.POSTGRES_DATABASE)

    bot = Bot(token=settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=storage)

    engine = create_async_engine(url=postgres_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    disp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))  # TODO: all log update to loguru
    # disp.update.middleware(ThrottlingMiddleware())

    disp.callback_query.middleware(CallbackAnswerMiddleware())

    disp.include_router(client.router)

    setup_dialogs(disp)

    disp.include_router(dialog)
    disp.include_router(main_menu)

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
