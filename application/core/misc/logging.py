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

# import logging.config
#
# import structlog
#
#
# def configure_logger():
#     timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False)
#     pre_chain = [
#         structlog.stdlib.add_log_level,
#         structlog.stdlib.ExtraAdder()
#     ]
#     logging.config.dictConfig({
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "plain": {
#                 "()": structlog.stdlib.ProcessorFormatter,
#                 "processors": [
#                     timestamper,
#                     structlog.stdlib.ProcessorFormatter.remove_processors_meta,
#                     structlog.dev.ConsoleRenderer(colors=False),
#                 ],
#                 "foreign_pre_chain": pre_chain,
#             },
#             "colored": {
#                 "()": structlog.stdlib.ProcessorFormatter,
#                 "processors": [
#                     timestamper,
#                     structlog.stdlib.ProcessorFormatter.remove_processors_meta,
#                     structlog.dev.ConsoleRenderer(colors=True),
#                 ],
#                 "foreign_pre_chain": pre_chain,
#             },
#         },
#         "handlers": {
#             "default": {
#                 "level": "INFO",
#                 "class": "logging.StreamHandler",
#                 "formatter": "colored",
#             },
#             "file": {
#                 "level": "DEBUG",
#                 "class": "logging.handlers.WatchedFileHandler",
#                 "filename": "debug.log",
#                 "formatter": "plain",
#             },
#         },
#         "loggers": {
#             "": {
#                 "handlers": ["default", "file"],
#                 "level": "DEBUG",
#                 "propagate": True,
#             },
#         }
#     })
#     structlog.configure(
#         processors=[
#             structlog.stdlib.add_log_level,
#             structlog.stdlib.PositionalArgumentsFormatter(),
#             timestamper,
#             structlog.processors.StackInfoRenderer(),
#             structlog.processors.format_exc_info,
#             structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
#         ],
#         logger_factory=structlog.stdlib.LoggerFactory(),
#         wrapper_class=structlog.stdlib.BoundLogger,
#         cache_logger_on_first_use=True,
#     )
#     logger: structlog.stdlib.BoundLogger = structlog.get_logger()
#     return logger
