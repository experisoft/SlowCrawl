import logging
import os
from pathlib import Path

def setup_logging():
    """
    Configure application-wide logging.
    Call this ONCE at application startup.
    """
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=os.getenv('LOG_LEVEL', 'INFO').upper(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'application.log'),
            logging.StreamHandler()
        ],
        force=True
    )
