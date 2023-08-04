import datetime

import lz4.frame
import orjson
import uuid6
from sqlalchemy import (
    select,
    func,
    delete
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from taskiq import (
    Context,
    TaskiqDepends,
)

from application.infrastructure.database.models import Service, User
from application.infrastructure.scheduler.tkq import broker


@broker.task(
    task_name='base_polling',
    schedule=[
        {
            'cron': '*/1 * * * *'  # 00 '12 * * *' and '00 16 * * * '
        },
    ],
)
async def base_polling_task(context: Context = TaskiqDepends()) -> None:
    nats_connect = context.state.nats
    async_engine = context.state.database

    jetstream = nats_connect.jetstream()
    async_session_maker: async_sessionmaker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=True,
        expire_on_commit=True,  # when you commit, load new object from database
    )

    async with async_session_maker() as session:
        async with session.begin():
            request = await session.scalars(
                select(Service)
                .where(
                    func.date(Service.reminder) == datetime.datetime.utcnow().date()
                )
            )
            services = request.all()

            for service in services:
                await jetstream.publish(
                    stream='service_notify',
                    subject='service_notify.message',
                    timeout=10,
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
