import logging

from rich.logging import RichHandler

__all__ = (
    "setup_logging",
    "get_logger",
)


def setup_logging() -> None:
    """Setup logging for the CLI."""

    logger = logging.getLogger("pywebp")

    handler = RichHandler(
        rich_tracebacks=True,
        omit_repeated_times=False,
        markup=False,
        show_path=False,
    )

    handler.setFormatter(logging.Formatter(fmt="%(message)s"))

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.debug("Logging setup complete")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name.replace("python_webp", "pywebp"))
