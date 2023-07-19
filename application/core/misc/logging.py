import logging
from types import FrameType

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame: FrameType | None = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

# import logging
# import structlog
# logger = structlog.get_logger()
#
# configure_logger(logging.getLogger(), "INFO")
#
# await logger.ainfo("LAUNCHING BOT")
#
# def configure_logger(logger, level):
#     structlog.configure(
#         processors=[
#             structlog.contextvars.merge_contextvars,
#             structlog.stdlib.PositionalArgumentsFormatter(),
#             structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
#             structlog.processors.StackInfoRenderer(),
#             structlog.processors.format_exc_info,
#             structlog.processors.add_log_level,
#             structlog.dev.ConsoleRenderer(),
#         ],
#         wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
#         context_class=dict,
#         logger_factory=structlog.PrintLoggerFactory(),
#         cache_logger_on_first_use=True
#     )
#
#     formatter = structlog.stdlib.ProcessorFormatter(
#         processor=structlog.dev.ConsoleRenderer()
#     )
#
#     handler = logging.StreamHandler()
#     handler.setFormatter(formatter)
#
#     logger.addHandler(handler)
#     logger.setLevel(level)
