import datetime
import logging

import nats
from ormsgpack.ormsgpack import packb
from sqlalchemy import select, delete
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
    session_maker: AsyncSession = async_sessionmaker(asyncio_engine, expire_on_commit=True)

    state.nats = nats_connect
    state.database = session_maker


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await state.nats.drain()


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def polling_base_task(context: Context = TaskiqDepends()) -> None:
    nats_connect = context.state.nats
    session_maker = context.state.database

    js = nats_connect.jetstream()

    async with session_maker() as session:
        async with session.begin():
            request = await session.execute(select(Service))
            result = request.scalars()

            for item in result:
                if item.reminder.date() == datetime.datetime.utcnow().date():
                    await js.publish(
                        subject="service_notify.message",
                        payload=packb({"user_id": item.service_by_user_id, "service": item.title})
                    )

                    await session.execute(delete(Service).where(Service.service_id == item.service_id))
                    await session.merge(User(user_id=item.service_by_user_id, count_subs=User.count_subs - 1))
