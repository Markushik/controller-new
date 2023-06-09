# -*- coding: utf-8 -*-
"""
The main file responsible for launching the bot
"""

import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from loguru import logger
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession
)

from application.core.config.config import settings
from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker
from application.infrastructure.stream.worker import poll_nats
from application.tgbot.dialogs.create_menu.dialog import create_menu
from application.tgbot.dialogs.main_menu.dialog import main_menu
from application.tgbot.handlers import client
from application.tgbot.handlers.errors import on_unknown_intent, on_unknown_state
from application.tgbot.middlewares.database import DbSessionMiddleware
from application.tgbot.middlewares.i18n import make_i18n_middleware


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

    storage: RedisStorage = RedisStorage.from_url(
        url=maker.redis_url.human_repr(),
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    asyncio_engine: AsyncEngine = create_async_engine(
        url=maker.database_url.human_repr(),
        pool_pre_ping=True,
        echo=False
    )
    session_maker: AsyncSession = async_sessionmaker(
        bind=asyncio_engine,
        class_=AsyncSession,
        expire_on_commit=True
    )

    bot: Bot = Bot(token=settings['API_TOKEN'], parse_mode=ParseMode.HTML)
    disp: Dispatcher = Dispatcher(storage=storage, events_isolation=storage.create_isolation())

    i18n_middleware = make_i18n_middleware()

    disp.message.middleware(i18n_middleware)
    disp.callback_query.middleware(i18n_middleware)

    disp.callback_query.middleware(CallbackAnswerMiddleware())
    disp.update.outer_middleware(DbSessionMiddleware(session_pool=session_maker))

    disp.include_routers(
        client.router,
        create_menu,
        main_menu,
    )
    disp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    disp.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))

    setup_dialogs(disp)

    logger.info("LAUNCHING BOT")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(poll_nats(bot), disp.start_polling(bot))
    finally:
        await storage.close()
        await asyncio_engine.dispose()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        logger.warning("SHUTDOWN BOT")
