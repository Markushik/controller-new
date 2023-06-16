import asyncio
import logging

from loguru import logger
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker
from taskiq_redis import RedisAsyncResultBackend


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)

broker = NatsBroker("nats://127.0.0.1:4222", queue="iop").with_result_backend(
    RedisAsyncResultBackend("redis://localhost/1")
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


# taskiq worker main:broker
# taskiq scheduler main:scheduler

@broker.task
async def heavy_task(value: int) -> int:
    print("ya zdes")
    return value + 1


async def main():
    await heavy_task.kiq(1)


if __name__ == "__main__":
    asyncio.run(main())
