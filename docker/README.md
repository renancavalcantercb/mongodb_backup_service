# Docker Configuration

Este diretório contém todos os arquivos relacionados ao Docker para o MongoDB Backup Service.

## Arquivos

- **`Dockerfile`** - Configuração da imagem Docker
- **`docker-compose.yml`** - Orquestração dos serviços
- **`.dockerignore`** - Arquivos ignorados durante o build

## Como usar

### Executar com Docker Compose

```bash
# A partir do diretório raiz do projeto
docker-compose -f docker/docker-compose.yml up --build
```

### Executar apenas o container

```bash
# Build da imagem
docker build -f docker/Dockerfile -t mongodb-backup-service .

# Executar o container
docker run -p 5000:5000 --env-file .env mongodb-backup-service
```

## Variáveis de Ambiente

Certifique-se de configurar as variáveis de ambiente necessárias no arquivo `.env` na raiz do projeto. 