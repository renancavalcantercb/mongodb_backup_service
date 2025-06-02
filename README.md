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

## Project Structure

```
mongodb-backup-service/
├── src/                          # Source code
│   ├── app/                      # Application layer
│   │   └── main.py              # Flask application and routes
│   ├── core/                     # Business logic layer
│   │   ├── backup.py            # Backup service implementation
│   │   └── config.py            # Configuration management
│   ├── infrastructure/           # Infrastructure layer (future)
│   └── tests/                    # Test layer
│       └── test_backup.py       # Integration tests
├── scripts/                      # Utility scripts
│   └── run_tests.py             # Test runner
├── docs/                         # Documentation
│   └── ARCHITECTURE.md         # Architecture documentation
├── app.py                        # Main entry point
├── Dockerfile                    # Container configuration
├── docker-compose.yml           # Container orchestration
└── README.md                    # Project documentation
```

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

### Local Development

Start the service:

```bash
python app.py
```

The service will be available at `http://localhost:5000`

### Docker

Build and run with Docker:

```bash
docker build -t mongodb-backup-service .
docker run -p 5000:5000 --env-file .env mongodb-backup-service
```

Or use Docker Compose:

```bash
docker-compose up --build
```

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

## Testing

Run tests using the test runner:

```bash
python scripts/run_tests.py
```

Or run tests directly:

```bash
python src/tests/test_backup.py
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

## Architecture

This project follows clean architecture principles with clear separation of concerns. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed information.

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
python app.py
```

To run backup directly (without Flask):

```bash
python -c "from src.core.backup import run_backup; run_backup()"
```
