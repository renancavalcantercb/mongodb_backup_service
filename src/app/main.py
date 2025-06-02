from flask import Flask, jsonify
from dotenv import load_dotenv
from src.core.backup import run_backup
from src.core.config import Config

# Carregar variáveis de ambiente
load_dotenv()
Config.validate()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "MongoDB Backup Service",
                "message": "Service is running properly",
            }
        ),
        200,
    )


@app.route("/trigger_backup", methods=["POST"])
def trigger_backup():
    """Trigger MongoDB backup process."""
    try:
        backup_summary = run_backup()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Backup executed successfully",
                    "summary": backup_summary,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": f"Backup failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
