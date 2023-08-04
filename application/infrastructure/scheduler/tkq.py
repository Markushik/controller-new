import logging

import nats
from loguru import logger
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
)
from taskiq import (
    TaskiqState,
    TaskiqEvents,
    TaskiqScheduler,
)
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker

logging.basicConfig(handlers=[InterceptHandler()], level='INFO')

broker = NatsBroker(
    servers=[
        maker.create_nats_url.human_repr(),
    ],
    subject='taskiq_tasks',
    queue='send_service',
)
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[
        LabelScheduleSource(broker=broker),
    ],
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    logger.info('Taskiq Launching')

    nats_connect = await nats.connect(maker.create_nats_url.human_repr())
    async_engine: AsyncEngine = create_async_engine(
        url=maker.create_postgres_url.human_repr(),
        pool_pre_ping=True,
        echo=False,
    )

    state.nats = nats_connect
    state.database = async_engine


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    logger.info('Taskiq Shutdown')

    await state.nats.drain()
    await state.database.dispose()
