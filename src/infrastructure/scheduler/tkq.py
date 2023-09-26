import nats
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from src.core.utils.builders import create_nats_url, create_postgres_url

broker = NatsBroker(
    servers=[
        create_nats_url().human_repr(),
    ],
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

    nats_connect = await nats.connect(
        servers=[
            create_nats_url().human_repr()
        ]
    )
    async_engine: AsyncEngine = create_async_engine(
        url=create_postgres_url().human_repr(),
        pool_pre_ping=True,
        echo=False,
    )

    state.nats = nats_connect
    state.database = async_engine


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    logger.warning('Taskiq Shutdown')

    await state.nats.drain()
    await state.database.dispose()
