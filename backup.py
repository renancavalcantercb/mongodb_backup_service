import os
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pymongo import MongoClient
from bson import json_util
import logging

from config import Config

Config.validate()

logging.basicConfig(level=Config.get_log_level(), format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)


class MongoBackupService:
    """MongoDB backup service with ZIP archive generation."""

    def __init__(self):
        self.mongo_uri = Config.MONGODB_URI
        self.database_name = Config.MONGODB_DATABASE
        self.backup_base_dir = Config.BACKUP_BASE_DIR

        if not self.mongo_uri:
            raise ValueError("MONGODB_URI environment variable is required")

    def get_mongo_client(self) -> MongoClient:
        """Establish connection to MongoDB Atlas."""
        try:
            client = MongoClient(self.mongo_uri)
            client.admin.command("ping")
            logger.info("Successfully connected to MongoDB Atlas")
            return client
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB Atlas: {e}")
            raise

    def create_backup_directory(self) -> tuple[Path, str]:
        """Create timestamped backup directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_base_dir / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created backup directory: {backup_dir}")
        return backup_dir, timestamp

    def backup_collection(
        self,
        collection,
        backup_dir: Path,
        db_name: str,
        collection_name: str,
        timestamp: str,
    ) -> Optional[Path]:
        """Backup a single collection to JSON file."""
        try:
            documents = list(collection.find())

            if not documents:
                logger.info(f"Collection {collection_name} is empty")
                return None

            filename = f"{timestamp}_{db_name}_{collection_name}.json"
            filepath = backup_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(
                    documents,
                    f,
                    default=json_util.default,
                    indent=2,
                    ensure_ascii=False,
                )

            logger.info(
                f"Backed up collection {collection_name} to {filepath} "
                f"({len(documents)} documents)"
            )
            return filepath

        except Exception as e:
            logger.error(f"Failed to backup collection {collection_name}: {e}")
            raise

    def create_zip_archive(self, backup_dir: Path, timestamp: str) -> Path:
        """Create ZIP archive from backup directory."""
        zip_filename = f"mongodb_backup_{timestamp}.zip"
        zip_path = self.backup_base_dir / zip_filename

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in backup_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(backup_dir)
                    zipf.write(file_path, arcname)

        logger.info(f"Created ZIP archive: {zip_path}")
        return zip_path

    def cleanup_backup_directory(self, backup_dir: Path) -> None:
        """Remove temporary backup directory after ZIP creation."""
        try:
            import shutil

            shutil.rmtree(backup_dir)
            logger.info(f"Cleaned up temporary directory: {backup_dir}")
        except Exception as e:
            logger.warning(f"Failed to cleanup directory {backup_dir}: {e}")

    def run_backup(self) -> Dict:
        """Execute complete backup process."""
        try:
            logger.info("Starting backup process...")

            client = self.get_mongo_client()
            backup_dir, timestamp = self.create_backup_directory()

            db = client[self.database_name]
            collections = db.list_collection_names()

            if not collections:
                logger.warning(f"No collections found in database {self.database_name}")
                return {
                    "status": "warning",
                    "message": "No collections found",
                    "timestamp": timestamp,
                }

            logger.info(f"Found {len(collections)} collections: {collections}")

            backup_summary = {
                "timestamp": datetime.now().isoformat(),
                "database": self.database_name,
                "collections_backed_up": [],
                "backup_directory": str(backup_dir),
                "zip_file": None,
                "total_collections": len(collections),
                "successful_backups": 0,
            }

            backed_up_files = []

            for collection_name in collections:
                try:
                    collection = db[collection_name]
                    file_path = self.backup_collection(
                        collection,
                        backup_dir,
                        self.database_name,
                        collection_name,
                        timestamp,
                    )
                    if file_path:
                        backup_summary["collections_backed_up"].append(collection_name)
                        backup_summary["successful_backups"] += 1
                        backed_up_files.append(file_path)
                except Exception as e:
                    logger.error(f"Failed to backup collection {collection_name}: {e}")
                    continue

            summary_file = backup_dir / f"{timestamp}_backup_summary.json"
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(backup_summary, f, indent=2, ensure_ascii=False)

            if backed_up_files:
                zip_path = self.create_zip_archive(backup_dir, timestamp)
                backup_summary["zip_file"] = str(zip_path)
                self.cleanup_backup_directory(backup_dir)

            client.close()

            logger.info(
                f"Backup completed successfully! "
                f"{backup_summary['successful_backups']}/{backup_summary['total_collections']} "
                f"collections backed up"
            )

            return backup_summary

        except Exception as e:
            logger.error(f"Backup process failed: {e}")
            raise


def run_backup() -> Dict:
    """Entry point for backup execution."""
    service = MongoBackupService()
    return service.run_backup()


if __name__ == "__main__":
    run_backup()
