# -*- coding: utf-8 -*-
"""
The main file responsible for launching the bot
"""

import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from loguru import logger
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infrastructure.utils.commands import set_commands
from app.infrastructure.utils.config import settings
from app.infrastructure.utils.logging import InterceptHandler
from app.tgbot.dialogs.create import dialog
from app.tgbot.dialogs.menu import main_menu
from app.tgbot.handlers import errors, client
from app.tgbot.middlewares.database import DbSessionMiddleware


async def main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logging.basicConfig(handlers=[InterceptHandler()], level='INFO')
    logger.add(
        '../../debug.log', format='{time} {level} {message}', level='INFO',
        colorize=True, encoding='utf-8', rotation='10 MB', compression='zip'
    )
    logger.info("LAUNCHING BOT")

    postgres_url = URL.create(
        drivername='postgresql+asyncpg', host=settings['postgres.POSTGRES_HOST'],
        port=settings['postgres.POSTGRES_PORT'], username=settings['postgres.POSTGRES_USERNAME'],
        password=settings['postgres.POSTGRES_PASSWORD'], database=settings['postgres.POSTGRES_DATABASE']
    )

    if settings['redis.USE_REDIS'] is True:
        storage = RedisStorage.from_url(
            url=f"redis://{settings['redis.REDIS_HOST']}:{settings['redis.REDIS_PORT']}/{settings['redis.REDIS_DATABASE']}",
            key_builder=DefaultKeyBuilder(with_destiny=True)
        )
    else:
        storage = MemoryStorage()

    engine = create_async_engine(url=postgres_url, echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=settings['API_TOKEN'], parse_mode=ParseMode.HTML)
    disp = Dispatcher(storage=storage)

    disp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    disp.callback_query.middleware(CallbackAnswerMiddleware())

    disp.include_routers(client.router, errors.router)
    disp.include_routers(dialog, main_menu)

    setup_dialogs(disp)

    try:
        await set_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await disp.start_polling(bot)
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")
