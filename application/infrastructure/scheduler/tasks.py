import datetime
import logging

import nats
from ormsgpack.ormsgpack import packb
from sqlalchemy import (
    select,
    delete,
    func
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from taskiq import (
    TaskiqState,
    TaskiqEvents,
    TaskiqDepends,
    TaskiqScheduler,
    Context
)
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker
from application.infrastructure.database.models.tables import Service, User

logging.basicConfig(handlers=[InterceptHandler()], level="INFO")

broker = NatsBroker([maker.nats_url.human_repr(), ], queue="send_service")
scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    nats_connect = await nats.connect(maker.nats_url.human_repr())
    asyncio_engine: AsyncEngine = create_async_engine(url=maker.database_url.human_repr(), echo=True)

    state.nats = nats_connect
    state.database = asyncio_engine


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await state.nats.drain()
    await state.database.dispose()


@broker.task(
    task_name="polling_base",
    schedule=[{"cron": "*/1 * * * *"}]  # 00 12 * * *
)
async def polling_base_task(context: Context = TaskiqDepends()) -> None:
    nats_connect = context.state.nats
    asyncio_engine = context.state.database

    jetstream = nats_connect.jetstream()
    session_maker = async_sessionmaker(asyncio_engine, expire_on_commit=True)

    async with session_maker() as session:
        async with session.begin():
            request = await session.execute(
                select(
                    Service.service_id,
                    Service.service_by_user_id,
                    User.language,
                    Service.title,
                    Service.reminder
                )
                .join(User, User.user_id == Service.service_by_user_id)
                .where(func.date(Service.reminder) == datetime.datetime.utcnow().date())
            )
            services = request.all()

            async for service in services:
                await jetstream.publish(
                    stream="service_notify",
                    timeout=10,
                    subject="service_notify.message",
                    payload=packb(
                        {
                            "user_id": service[1],
                            "language": service[2],
                            "service_name": service[3],
                        }
                    ),
                    headers={
                        'Foo': 'Bar'
                    }
                )

                await session.execute(delete(Service).where(Service.service_id == service[0]))
                await session.merge(User(user_id=service.service_by_user_id, count_subs=User.count_subs - 1))

    await session.commit()
    await session.close()
