"""
Logging configuration for DSA Mentor application.
"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = None, log_file: str = "dsa_mentor.log", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure logger for the application.
    
    Args:
        name: Logger name (defaults to calling module)
        log_file: Log file path
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not setup file logging: {e}")
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance for the calling module.
    
    Args:
        name: Logger name (defaults to calling module)
        
    Returns:
        Logger instance
    """
    return setup_logger(name)


# Default application logger
app_logger = setup_logger("dsa_mentor") 