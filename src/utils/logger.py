"""Logging configuration."""

import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from src.config import ROOT_DIR


def setup_logger(
    name: str = "ds-project",
    log_file: Optional[str] = None,
    level: str = "INFO",
    rotation: str = "10 MB",
    retention: str = "1 month"
) -> logger:
    """
    Set up logger with file and console output.

    Args:
        name: Logger name
        log_file: Log file path (optional)
        level: Logging level
        rotation: When to rotate log file
        retention: How long to keep old logs

    Returns:
        Configured logger
    """
    # Remove default logger
    logger.remove()

    # Console logger
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        colorize=True
    )

    # File logger (if specified)
    if log_file:
        log_path = ROOT_DIR / "logs" / log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            str(log_path),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation=rotation,
            retention=retention,
            compression="zip"
        )

    return logger


# Default logger instance
log = setup_logger(log_file="app.log")
