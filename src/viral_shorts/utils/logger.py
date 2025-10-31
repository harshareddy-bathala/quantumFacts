"""
Logger utility module
Sets up colored logging for the application
"""

import logging
import sys
from pathlib import Path
from typing import Optional

try:
    import colorlog
    HAS_COLORLOG = True
except ImportError:
    HAS_COLORLOG = False

from ..config import LOG_LEVEL, LOG_FORMAT, LOG_FILE


def setup_logger(name: str, log_file: Optional[Path] = None, level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with colored console output and file logging
    
    Args:
        name: Logger name (usually __name__)
        log_file: Path to log file (uses config default if not provided)
        level: Log level (uses config default if not provided)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level
    log_level = getattr(logging, (level or LOG_LEVEL).upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if HAS_COLORLOG:
        # Colored formatter
        color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(color_formatter)
    else:
        # Standard formatter
        formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # File handler
    log_file_path = log_file or LOG_FILE
    if log_file_path:
        try:
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name) if logging.getLogger(name).handlers else setup_logger(name)
