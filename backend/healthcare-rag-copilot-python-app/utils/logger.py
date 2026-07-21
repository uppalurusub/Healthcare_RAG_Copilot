from pathlib import Path
from loguru import logger
import sys

# Create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Remove default logger
logger.remove()

# Console Logger
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
)

# Application Logs
logger.add(
    "logs/healthcare.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
)

# Error Logs
logger.add(
    "logs/error.log",
    level="ERROR",
    rotation="5 MB",
    retention="60 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)


def get_logger():
    return logger