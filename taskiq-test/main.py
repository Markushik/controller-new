from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from taskiq_redis import RedisAsyncResultBackend

broker = NatsBroker("nats://127.0.0.1:4222", queue="iop").with_result_backend(
    RedisAsyncResultBackend("redis://localhost/1")
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


@broker.task(schedule=[{"cron": "*/1 * * * *", "args": [1]}])
async def heavy_task(value: int) -> int:
    print("AAAA")
    return value + 1
