import logging
import sys
from pathlib import Path
from ..config import settings

def setup_logging():
    """Configure logging for the application."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = getattr(logging, settings.LOG_LEVEL.upper())
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.BASE_DIR) / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / "vpm.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    
    return logger

# Create a default logger instance
logger = setup_logging() 