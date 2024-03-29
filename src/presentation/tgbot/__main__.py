"""
The main file responsible for launching the bot
"""

import asyncio
import logging

import nats
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from loguru import logger
from nats.aio.client import Client
from nats.js import JetStreamContext
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from src.core.config.parser import settings
from src.core.utils.builders import create_postgres_url, create_nats_url, create_redis_url
from src.core.utils.logging import InterceptHandler
from src.infrastructure.stream.worker import nats_polling
from src.presentation.tgbot.dialogs.create_menu.dialog import create_menu
from src.presentation.tgbot.dialogs.delete_menu.dialog import delete_menu
from src.presentation.tgbot.dialogs.edit_menu.dialog import edit_menu
from src.presentation.tgbot.dialogs.main_menu.dialog import main_menu
from src.presentation.tgbot.handlers import client, errors
from src.presentation.tgbot.middlewares.database import DbSessionMiddleware
from src.presentation.tgbot.middlewares.i18n import I18nMiddleware, make_i18n_middleware


async def _main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logging.basicConfig(
        handlers=[
            InterceptHandler()
        ],
        level='DEBUG',
        force=True
    )
    logger.add(
        sink='../../../debug.log',
        format='{time} | {level} | {message}',
        level='DEBUG',
        enqueue=True,
        colorize=True,
        encoding='utf-8',
        rotation='10 MB',
        compression='zip'
    )

    async_engine: AsyncEngine = create_async_engine(
        url=create_postgres_url().human_repr(),
        pool_pre_ping=True,
        echo=False,
    )
    async_session_maker: async_sessionmaker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=True,
        expire_on_commit=True,
    )

    nats_client: Client = await nats.connect(
        servers=[
            create_nats_url().human_repr()
        ],
    )
    jetstream: JetStreamContext = nats_client.jetstream()

    storage: RedisStorage = RedisStorage.from_url(
        url=create_redis_url().human_repr(),
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
            with_bot_id=True
        ),
    )
    bot: Bot = Bot(
        token=settings['API_TOKEN'], parse_mode=ParseMode.HTML
    )
    disp: Dispatcher = Dispatcher(
        storage=storage, events_isolation=storage.create_isolation()
    )

    i18n_middleware: I18nMiddleware = make_i18n_middleware()

    disp.message.middleware(i18n_middleware)
    disp.callback_query.middleware(i18n_middleware)
    disp.update.outer_middleware(
        DbSessionMiddleware(session_maker=async_session_maker)
    )

    disp.include_router(client.router)
    disp.include_routers(
        main_menu,
        create_menu,
        delete_menu,
        edit_menu,
    )
    disp.errors.register(errors.on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    disp.errors.register(errors.on_unknown_state, ExceptionTypeFilter(UnknownState))

    setup_dialogs(disp)

    logger.info('Bot Launching')

    try:
        await jetstream.add_stream(
            name='service_notify',
            subjects=['service_notify.*'],
            retention='interest',
            storage='file'
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(
            nats_polling(
                bot=bot,
                i18n_middleware=i18n_middleware,
                jetstream=jetstream
            ),
            disp.start_polling(bot),
        )
    finally:
        await storage.close()
        await bot.session.close()
        await async_engine.dispose()
        await nats_client.drain()
        await logger.complete()


if __name__ == '__main__':
    try:
        asyncio.run(_main())
    except (SystemExit, KeyboardInterrupt):
        logger.warning('Bot Shutdown')
