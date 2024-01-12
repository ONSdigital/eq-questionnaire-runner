#!/usr/bin/env python
import logging
import os
import sys

from dotenv import load_dotenv
from structlog import configure, contextvars
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, TimeStamper, format_exc_info
from structlog.stdlib import LoggerFactory, add_log_level

from app.utilities.json import json_dumps

# Load environment variables from .env file
load_dotenv()


def configure_logging():
    log_level = logging.INFO
    debug = os.getenv("FLASK_DEBUG") == "1"
    if debug:
        log_level = logging.DEBUG

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(log_level)
    log_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

    error_log_handler = logging.StreamHandler(sys.stderr)
    error_log_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=log_level, format="%(message)s", handlers=[error_log_handler, log_handler]
    )

    # Set werkzeug logging level
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(level=log_level)

    def parse_exception(_, __, event_dict):
        if debug:
            return event_dict
        exception = event_dict.get("exception")
        if exception:
            event_dict["exception"] = exception.replace('"', "'").split("\n")
        return event_dict

    # setup file logging
    renderer_processor = (
        ConsoleRenderer() if debug else JSONRenderer(serializer=json_dumps)
    )
    processors = [
        contextvars.merge_contextvars,
        add_log_level,
        TimeStamper(key="created", fmt="iso"),
        add_service,
        format_exc_info,
        parse_exception,
        renderer_processor,
    ]

    configure(
        logger_factory=LoggerFactory(),
        processors=processors,
        cache_logger_on_first_use=True,
    )


def add_service(logger, method_name, event_dict):  # pylint: disable=unused-argument
    """
    Add the service name to the event dict.
    """
    event_dict["service"] = "eq-questionnaire-runner"
    return event_dict


# Initialise logging before the rest of the application
configure_logging()
from app.setup import (  # NOQA isort:skip # pylint: disable=wrong-import-position
    create_app,
)

application = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(port=port, threaded=True)
