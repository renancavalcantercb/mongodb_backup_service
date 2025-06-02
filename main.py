import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from backup import run_backup

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    """Endpoint de verificação de saúde do serviço"""
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "MongoDB Backup Service",
                "message": "Serviço funcionando corretamente",
            }
        ),
        200,
    )


@app.route("/trigger_backup", methods=["POST"])
def trigger_backup():
    """Endpoint para disparar o backup das coleções do MongoDB"""
    try:
        backup_summary = run_backup()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Backup executado com sucesso",
                    "summary": backup_summary,
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Erro durante o backup: {str(e)}"}),
            500,
        )


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
