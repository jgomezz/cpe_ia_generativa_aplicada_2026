# Ejecución de Qdrant en Docker

### 1. El servicio de Docker debe estar ejecutandose

### 2. Debe tener el archivo docker-compose.yml

```yml

name: qdrant_local

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"   # REST API + Dashboard web
      - "6334:6334"   # gRPC (opcional, más rápido)
    volumes:
      - ./qdrant_storage:/qdrant/storage  

```

### 3. En la carpeta donde se encuentra el archivo docker-compose.yml ejecutar el comando

```bash
docker compose up -d
```
### 4. Ingresar al enlace http://localhost:6333/dashboard#/welcome