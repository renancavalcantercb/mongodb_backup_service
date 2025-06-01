# MongoDB Backup Service

Flask service to backup all collections from a MongoDB Atlas database into JSON files and create ZIP archives.

## Features

- Flask endpoint to trigger backup via HTTP POST
- Connects to MongoDB Atlas
- Backs up all database collections
- Saves each collection in separate JSON files with timestamps
- Creates organized directories by timestamp
- Generates ZIP archives for easy storage and transfer
- Automatic cleanup of temporary directories
- Detailed logging throughout the process
- Robust error handling

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd mongodb-backup-service
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp env.example .env
```

4. Edit the `.env` file with your settings:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=your_database_name
FLASK_PORT=5000
FLASK_ENV=development
```

## Usage

### Start the service

```bash
python main.py
```

The service will be available at `http://localhost:5000`

### Available endpoints

#### 1. Health Check

```http
GET /
```

Response:

```json
{
  "status": "healthy",
  "service": "MongoDB Backup Service",
  "message": "Service is running properly"
}
```

#### 2. Trigger Backup

```http
POST /trigger_backup
```

Success response:

```json
{
  "status": "success",
  "message": "Backup executed successfully",
  "summary": {
    "timestamp": "2024-01-15T10:30:00.123456",
    "database": "database_name",
    "collections_backed_up": ["collection1", "collection2", "collection3"],
    "backup_directory": "backups/backup_20240115_103000",
    "zip_file": "backups/mongodb_backup_20240115_103000.zip",
    "total_collections": 3,
    "successful_backups": 3
  }
}
```

Error response:

```json
{
  "status": "error",
  "message": "Backup failed: Error details"
}
```

### Usage examples with curl

```bash
# Health check
curl http://localhost:5000/

# Trigger backup
curl -X POST http://localhost:5000/trigger_backup
```

## Backup Structure

Backups are saved with the following structure:

```
backups/
├── mongodb_backup_20240115_103000.zip
└── (temporary directories are cleaned up after ZIP creation)
```

### ZIP Archive Contents

```
20240115_103000_backup_summary.json
20240115_103000_database_name_collection1.json
20240115_103000_database_name_collection2.json
20240115_103000_database_name_collection3.json
```

### Backup Summary File

```json
{
  "timestamp": "2024-01-15T10:30:00.123456",
  "database": "database_name",
  "collections_backed_up": ["collection1", "collection2", "collection3"],
  "backup_directory": "backups/backup_20240115_103000",
  "zip_file": "backups/mongodb_backup_20240115_103000.zip",
  "total_collections": 3,
  "successful_backups": 3
}
```

## MongoDB Atlas Configuration

1. Access [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create a cluster (if you don't have one)
3. Configure network access (IP whitelist)
4. Create a database user
5. Get the connection string in the format:

   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

## Environment Variables

| Variable           | Description                                | Required | Default       |
| ------------------ | ------------------------------------------ | -------- | ------------- |
| `MONGODB_URI`      | MongoDB Atlas connection string            | Yes      | -             |
| `MONGODB_DATABASE` | Database name                              | No       | `default_db`  |
| `FLASK_PORT`       | Flask server port                          | No       | `5000`        |
| `FLASK_ENV`        | Flask environment (development/production) | No       | `development` |

## Logging

The service generates detailed logs during the backup process:

```
2024-01-15 10:30:00,123 - backup - INFO - Starting backup process...
2024-01-15 10:30:00,456 - backup - INFO - Successfully connected to MongoDB Atlas
2024-01-15 10:30:00,789 - backup - INFO - Created backup directory: backups/backup_20240115_103000
2024-01-15 10:30:01,012 - backup - INFO - Found 3 collections: ['collection1', 'collection2', 'collection3']
2024-01-15 10:30:01,345 - backup - INFO - Backed up collection collection1 to backups/backup_20240115_103000/20240115_103000_database_name_collection1.json (150 documents)
2024-01-15 10:30:01,678 - backup - INFO - Backed up collection collection2 to backups/backup_20240115_103000/20240115_103000_database_name_collection2.json (75 documents)
2024-01-15 10:30:01,901 - backup - INFO - Backed up collection collection3 to backups/backup_20240115_103000/20240115_103000_database_name_collection3.json (300 documents)
2024-01-15 10:30:02,234 - backup - INFO - Created ZIP archive: backups/mongodb_backup_20240115_103000.zip
2024-01-15 10:30:02,567 - backup - INFO - Cleaned up temporary directory: backups/backup_20240115_103000
2024-01-15 10:30:02,890 - backup - INFO - Backup completed successfully! 3/3 collections backed up
```

## Error Handling

The service handles the following error scenarios:

- MongoDB Atlas connection failure
- Database not found
- Empty or non-existent collections
- File write permission issues
- Missing environment variables
- ZIP archive creation failures

## Development

To run in development mode:

```bash
export FLASK_ENV=development
python main.py
```

To run backup directly (without Flask):

```bash
python backup.py
```

To run tests:

```bash
python test_backup.py
```

## Dependencies

- **Flask**: Web framework for creating endpoints
- **pymongo**: Official MongoDB driver for Python
- **python-dotenv**: Environment variable loading
- **requests**: HTTP library for testing

## Architecture

The service uses a class-based approach with the `MongoBackupService` class that encapsulates all backup functionality:

- **Separation of concerns**: Each method has a single responsibility
- **Type hints**: Full type annotation for better code quality
- **Error handling**: Comprehensive exception handling
- **Logging**: Detailed logging throughout the process
- **Resource cleanup**: Automatic cleanup of temporary files
- **Modern Python**: Uses pathlib, f-strings, and other modern features

## License

This project is under the MIT License.
