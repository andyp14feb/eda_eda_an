# logger_utils.py
import logging

def setup_logger(name: str) -> logging.Logger:
    """
    📘 Create and configure a logger with a consistent format.

    Parameters:
        name (str): The logger's name (usually the function/module name)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with standard format.

    Parameters:
        name (str): Name of the logger, usually __name__.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger