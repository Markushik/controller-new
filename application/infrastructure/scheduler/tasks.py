import datetime
import logging

import nats
from ormsgpack.ormsgpack import packb
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from taskiq import TaskiqScheduler, TaskiqState, TaskiqEvents, Context, TaskiqDepends
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker
from taskiq_redis import RedisAsyncResultBackend

from application.core.misc.logging import InterceptHandler
from application.core.misc.makers import maker
from application.infrastructure.database.models import Service, User

# taskiq worker application.infrastructure.scheduler.tasks:broker
# taskiq scheduler application.infrastructure.scheduler.tasks:scheduler

logging.basicConfig(handlers=[InterceptHandler()], level="INFO")

broker = NatsBroker(str(maker.nats_url), queue="i_am_queue").with_result_backend(
    RedisAsyncResultBackend("redis://localhost/1")
)
scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    nc = await nats.connect(str(maker.nats_url))

    engine: AsyncEngine = create_async_engine(url=str(maker.database_url), echo=False)
    session_maker: AsyncSession = async_sessionmaker(engine, expire_on_commit=True)

    state.nats = nc
    state.database = session_maker


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await state.nats.drain()


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def polling_base_task(context: Context = TaskiqDepends()):
    nc = context.state.nats
    session_maker = context.state.database

    js = nc.jetstream()

    async with session_maker() as session:
        async with session.begin():
            request = await session.execute(select(Service))
            result = request.scalars()

            for item in result:
                if item.reminder.date() == datetime.datetime.utcnow().date():
                    await js.publish(
                        subject="service_notify.message",
                        payload=packb(list((item.service_by_user_id, item.title)))
                    )

                    await session.execute(delete(Service).where(Service.service_id == item.service_id))
                    await session.merge(User(user_id=item.service_by_user_id, count_subs=User.count_subs - 1))
