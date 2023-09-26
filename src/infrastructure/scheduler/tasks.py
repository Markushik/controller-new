import datetime

import ormsgpack
import uuid6
import zstd
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload
from taskiq import Context, TaskiqDepends

from ..database.models.schemas import Service, User
from ..scheduler.tkq import broker


@broker.task(
    task_name='base_polling',
    schedule=[
        {
            "cron": "*/1 * * * *",
            "cron_offset": "Europe/Moscow"
        },
        {
            "cron": "0 12 * * *",
            "cron_offset": "Europe/Moscow"
        },
        {
            "cron": "0 16 * * *",
            "cron_offset": "Europe/Moscow"
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
        request = await session.scalars(
            select(Service)
            .options(
                joinedload(Service.user)
            )
            .where(
                func.date(Service.reminder) == datetime.datetime.utcnow().date()
            )
        )
        services = request.all()
        identifiers = list()

    for service in services:
        await jetstream.publish(
            subject='service_notify.message',
            payload=zstd.compress(
                ormsgpack.packb(
                    {
                        'chat_id': service.user.chat_id,
                        'language': service.user.language,
                        'service': service.title,
                        'months': service.months
                    }
                )
            ),
            headers={
                'Nats-Msg-Id': uuid6.uuid8().hex,  # uuid8, because uniqueness guarantee
            },
        )
        await session.merge(
            User(
                user_id=service.user.user_id,
                count_subs=User.count_subs - 1,
            )
        )
        identifiers.append(service.service_id)

    await session.execute(
        delete(Service).where(Service.service_id.in_(identifiers))
    )
    await session.commit()
