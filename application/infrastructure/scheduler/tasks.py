import datetime
import logging

import lz4.frame
import nats
import orjson
import uuid6
from loguru import logger
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from taskiq import (
    Context,
    TaskiqState,
    TaskiqEvents,
    TaskiqDepends,
    TaskiqScheduler,
)
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker
from application.infrastructure.database.models import Service, User

logging.basicConfig(handlers=[InterceptHandler()], level='INFO')

broker = NatsBroker(
    servers=[
        maker.create_nats_url.human_repr(),
    ],
    queue='send_service',
)
scheduler = TaskiqScheduler(
    broker=broker, sources=[LabelScheduleSource(broker)]
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    logger.info('Taskiq Launching')

    nats_connect = await nats.connect(maker.create_nats_url.human_repr())
    async_engine: AsyncEngine = create_async_engine(
        url=maker.create_postgres_url.human_repr(),
        pool_pre_ping=True,
        echo=False,
        connect_args={'server_settings': {'jit': 'off'}},
    )

    state.nats = nats_connect
    state.database = async_engine


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    logger.info('Taskiq Shutdown')

    await state.nats.drain()
    await state.database.dispose()


@broker.task(
    task_name='base_polling', schedule=[{'cron': '*/1 * * * *'}]  # 00 12 * * *
)
async def base_polling_task(context: Context = TaskiqDepends()) -> None:
    nats_connect = context.state.nats
    async_engine = context.state.database

    jetstream = nats_connect.jetstream()
    async_session: AsyncSession = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=True,  # when you commit, load new object from database
    )

    async with async_session() as session:
        async with session.begin():
            request = await session.scalars(
                select(Service).where(
                    func.date(Service.reminder)
                    == datetime.datetime.utcnow().date()
                )
            )
            services = request.all()

            for service in services:
                await jetstream.publish(
                    stream='service_notify',
                    timeout=10,
                    subject='service_notify.message',
                    payload=lz4.frame.compress(  # compress data (read the lz4 technology)
                        orjson.dumps(  # or you can use ormsgpack
                            {
                                'user_id': service.user.user_id,
                                'language': service.user.language,
                                'service_name': service.title,
                            }
                        )
                    ),
                    headers={
                        'Nats-Msg-Id': uuid6.uuid8().hex,  # uuid8, because uniqueness guarantee
                    },
                )

                await session.execute(
                    delete(Service).where(
                        Service.service_id == service.service_id
                    )
                )
                await session.merge(
                    User(
                        user_id=service.service_fk,
                        count_subs=User.count_subs - 1,
                    )
                )

    await session.commit()
    await session.close()
