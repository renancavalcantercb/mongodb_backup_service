import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration class."""

    # MongoDB Configuration
    MONGODB_URI: Optional[str] = os.getenv("MONGODB_URI")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "default_db")

    # Flask Configuration
    FLASK_PORT: int = int(os.getenv("FLASK_PORT", 5000))
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG: bool = FLASK_ENV == "development"

    # Backup Configuration
    BACKUP_BASE_DIR: Path = Path("backups")
    BACKUP_RETENTION_DAYS: int = int(os.getenv("BACKUP_RETENTION_DAYS", 30))

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is required")

    @classmethod
    def get_log_level(cls) -> int:
        """Get numeric log level."""
        import logging

        return getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
