import datetime
import logging

import nats
from ormsgpack.ormsgpack import packb
from sqlalchemy import URL, select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker
from taskiq_redis import RedisAsyncResultBackend

from application.core.misc.logging import InterceptHandler
from application.infrastructure.database.models import Services, Users

# taskiq worker application.infrastructure.scheduler.tasks:broker
# taskiq scheduler application.infrastructure.scheduler.tasks:scheduler

logging.basicConfig(handlers=[InterceptHandler()], level="INFO")

broker = NatsBroker("nats://127.0.0.1:4222", queue="i_am_queue").with_result_backend(
    RedisAsyncResultBackend("redis://localhost/1")
)
scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def heavy_task():
    nc = await nats.connect('nats://127.0.0.1:4222')
    js = nc.jetstream()

    postgres_url = URL.create(drivername='postgresql+asyncpg', host="localhost", port="5432",
                              username="postgres", password="postgres", database="postgres")
    engine = create_async_engine(url=postgres_url, echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        async with session.begin():
            request = await session.execute(select(Services))
            result = request.scalars()

            for item in result:
                if item.reminder.date() == datetime.datetime.utcnow().date():
                    await js.publish(
                        subject="service_notify.message",
                        payload=packb(list((item.service_by_user_id, item.title)))
                    )
                    await session.execute(delete(Services).where(Services.service_id == item.service_id))  # noqa: E501
                    await session.merge(
                        Users(
                            user_id=item.service_by_user_id,
                            count_subs=Users.count_subs - 1
                        )
                    )
