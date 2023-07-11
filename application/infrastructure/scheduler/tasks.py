import datetime
import logging

import nats
from ormsgpack.ormsgpack import packb
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from taskiq import TaskiqScheduler, TaskiqState, TaskiqEvents, Context, TaskiqDepends
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker
from application.infrastructure.database.models import Service, User

logging.basicConfig(handlers=[InterceptHandler()], level="INFO")

broker = NatsBroker([maker.nats_url.human_repr()], queue="send_service")
scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    nats_connect = await nats.connect(maker.nats_url.human_repr())
    asyncio_engine: AsyncEngine = create_async_engine(url=maker.database_url.human_repr(), echo=False)

    state.nats = nats_connect
    state.database = asyncio_engine


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await state.nats.drain()
    await state.database.dispose()


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def polling_base_task(context: Context = TaskiqDepends()) -> None:
    nats_connect = context.state.nats
    asyncio_engine = context.state.database

    js = nats_connect.jetstream()
    session_maker: AsyncSession = async_sessionmaker(asyncio_engine, expire_on_commit=True)

    async with session_maker() as session:
        async with session.begin():
            request = await session.execute(
                select(Service).
                where(func.date(Service.reminder) == datetime.datetime.utcnow().date())
            )
            result = request.scalars()

            for item in result:
                await js.publish(
                    stream="service_notify",
                    timeout=30,
                    subject="service_notify.message",
                    payload=packb({"user_id": item.service_by_user_id, "service": item.title})
                )

                await session.execute(delete(Service).where(Service.service_id == item.service_id))
                await session.merge(User(user_id=item.service_by_user_id, count_subs=User.count_subs - 1))

        await session.close()
