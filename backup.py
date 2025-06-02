import os
import json
from datetime import datetime
from pymongo import MongoClient
from bson import json_util
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_mongo_client():
    """
    Cria e retorna uma conexão com o MongoDB Atlas
    """
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_URI não encontrada nas variáveis de ambiente")

    try:
        client = MongoClient(mongo_uri)
        # Testa a conexão
        client.admin.command("ping")
        logger.info("Conexão com MongoDB Atlas estabelecida com sucesso")
        return client
    except Exception as e:
        logger.error(f"Erro ao conectar com MongoDB Atlas: {e}")
        raise


def create_backup_directory():
    """
    Cria o diretório de backup se não existir
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/backup_{timestamp}"

    os.makedirs(backup_dir, exist_ok=True)
    logger.info(f"Diretório de backup criado: {backup_dir}")
    return backup_dir


def backup_collection(collection, backup_dir, db_name, collection_name):
    """
    Faz backup de uma coleção específica
    """
    try:
        # Obter todos os documentos da coleção
        documents = list(collection.find())

        if not documents:
            logger.info(f"Coleção {collection_name} está vazia")
            return

        # Nome do arquivo JSON
        filename = f"{db_name}_{collection_name}.json"
        filepath = os.path.join(backup_dir, filename)

        # Salvar documentos em JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                documents, f, default=json_util.default, indent=2, ensure_ascii=False
            )

        logger.info(
            f"Backup da coleção {collection_name} salvo em {filepath} ({len(documents)} documentos)"
        )

    except Exception as e:
        logger.error(f"Erro ao fazer backup da coleção {collection_name}: {e}")
        raise


def run_backup():
    """
    Função principal que executa o backup de todas as coleções
    """
    try:
        logger.info("Iniciando processo de backup...")

        # Conectar ao MongoDB
        client = get_mongo_client()

        # Criar diretório de backup
        backup_dir = create_backup_directory()

        # Obter nome do banco de dados (pode ser configurado via env var)
        database_name = os.getenv("MONGODB_DATABASE", "default_db")
        db = client[database_name]

        # Obter lista de todas as coleções
        collections = db.list_collection_names()

        if not collections:
            logger.warning(f"Nenhuma coleção encontrada no banco {database_name}")
            return

        logger.info(
            f"Encontradas {len(collections)} coleções para backup: {collections}"
        )

        # Fazer backup de cada coleção
        backup_summary = {
            "timestamp": datetime.now().isoformat(),
            "database": database_name,
            "collections_backed_up": [],
            "backup_directory": backup_dir,
        }

        for collection_name in collections:
            try:
                collection = db[collection_name]
                backup_collection(
                    collection, backup_dir, database_name, collection_name
                )
                backup_summary["collections_backed_up"].append(collection_name)
            except Exception as e:
                logger.error(f"Falha no backup da coleção {collection_name}: {e}")
                continue

        # Salvar resumo do backup
        summary_file = os.path.join(backup_dir, "backup_summary.json")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(backup_summary, f, indent=2, ensure_ascii=False)

        logger.info(f"Backup concluído com sucesso! Resumo salvo em {summary_file}")

        # Fechar conexão
        client.close()

        return backup_summary

    except Exception as e:
        logger.error(f"Erro durante o processo de backup: {e}")
        raise


if __name__ == "__main__":
    # Para teste direto do script
    run_backup()
