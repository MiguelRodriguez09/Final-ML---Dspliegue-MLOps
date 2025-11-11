# Carpeta: Docker

## 1. Propósito

Esta carpeta contiene **todos los archivos de containerización** necesarios para desplegar el proyecto MLOps usando Docker:
- Dockerfiles para diferentes servicios
- Docker Compose para orquestación
- Scripts de inicio
- Configuraciones de contenedores

---

## 2. Estructura de la Carpeta

```
docker/
├── Dockerfile                  # Dockerfile principal para la API Flask
├── Dockerfile.frontend         # Dockerfile para el frontend web
├── Dockerfile.streamlit        # Dockerfile para el dashboard Streamlit
├── docker-compose.yml          # Orquestación de todos los servicios (producción)
├── docker-compose.dev.yml      # Configuración para desarrollo
└── scripts/
    ├── docker-start.sh         # Script de inicio para Linux/Mac
    └── docker-start.bat        # Script de inicio para Windows
```

---

## 3. Descripción de Archivos

### 3.1. `Dockerfile` (API Principal)

**Propósito:** Containerizar la API Flask de predicciones.

**Contenido:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY mlops_pipeline/ ./mlops_pipeline/
COPY models/ ./models/
COPY data/metadata/ ./data/metadata/

# Exponer puerto
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando de inicio
CMD ["python", "-m", "mlops_pipeline.src.model_deploy"]
```

**Imagen base:** `python:3.10-slim` (ligera)

**Puerto expuesto:** 5000

**Servicios incluidos:**
- API Flask
- Modelo ML cargado
- Preprocessor cargado

---

### 3.2. `Dockerfile.streamlit`

**Propósito:** Containerizar el dashboard de monitoreo.

**Contenido:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY mlops_pipeline/ ./mlops_pipeline/
COPY data/ ./data/

# Exponer puerto de Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando de inicio
CMD ["streamlit", "run", "mlops_pipeline/src/streamlit_app.py", \
     "--server.address", "0.0.0.0", \
     "--server.port", "8501"]
```

**Puerto expuesto:** 8501

**Servicios incluidos:**
- Dashboard Streamlit
- Visualizaciones de drift
- Alertas y métricas

---

### 3.3. `Dockerfile.frontend`

**Propósito:** Containerizar la interfaz web HTML/JS.

**Contenido:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copiar frontend
COPY frontend/ ./frontend/

# Exponer puerto
EXPOSE 3000

# Comando de inicio (servidor Python simple)
CMD ["python", "-m", "http.server", "3000", "--directory", "frontend"]
```

**Puerto expuesto:** 3000

**Servicios incluidos:**
- Servidor HTTP simple
- Interfaz HTML/JS
- Formulario de predicción

---

### 3.4. `docker-compose.yml`

**Propósito:** Orquestar todos los servicios del proyecto.

**Contenido:**
```yaml
version: '3.8'

services:
  # Servicio de API Flask
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: mlops-api
    ports:
      - "5000:5000"
    volumes:
      - ../models:/app/models:ro
      - ../data:/app/data:ro
    environment:
      - FLASK_ENV=production
      - LOG_LEVEL=INFO
    restart: unless-stopped
    networks:
      - mlops-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Dashboard de Streamlit
  dashboard:
    build:
      context: ..
      dockerfile: docker/Dockerfile.streamlit
    container_name: mlops-dashboard
    ports:
      - "8501:8501"
    volumes:
      - ../data:/app/data
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - mlops-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend Web
  frontend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    container_name: mlops-frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - mlops-network

networks:
  mlops-network:
    driver: bridge

volumes:
  model-data:
  app-data:
```

**Servicios definidos:**
1. **api** - API Flask en puerto 5000
2. **dashboard** - Streamlit en puerto 8501
3. **frontend** - Interfaz web en puerto 3000

**Características:**
- Red compartida (`mlops-network`)
- Volúmenes para persistencia
- Health checks automáticos
- Auto-restart en caso de fallo

---

### 3.5. `docker-compose.dev.yml`

**Propósito:** Configuración para desarrollo con hot-reload.

**Diferencias con producción:**
```yaml
services:
  api:
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    volumes:
      - ../mlops_pipeline:/app/mlops_pipeline  # Hot-reload
    command: ["flask", "run", "--host=0.0.0.0", "--reload"]
```

---

## 4. Comandos de Docker

### 4.1. Construcción de Imágenes

```powershell
# Construir imagen de la API
docker build -f docker/Dockerfile -t mlops-api:latest .

# Construir imagen del dashboard
docker build -f docker/Dockerfile.streamlit -t mlops-dashboard:latest .

# Construir imagen del frontend
docker build -f docker/Dockerfile.frontend -t mlops-frontend:latest .

# Construir todas con Docker Compose
docker-compose -f docker/docker-compose.yml build
```

### 4.2. Ejecución de Contenedores

**Opción 1: Contenedores individuales**
```powershell
# Ejecutar solo API
docker run -d -p 5000:5000 --name mlops-api mlops-api:latest

# Ejecutar solo dashboard
docker run -d -p 8501:8501 --name mlops-dashboard mlops-dashboard:latest

# Ejecutar solo frontend
docker run -d -p 3000:3000 --name mlops-frontend mlops-frontend:latest
```

**Opción 2: Docker Compose (Recomendado)**
```powershell
# Iniciar todos los servicios
docker-compose -f docker/docker-compose.yml up -d

# Ver logs
docker-compose -f docker/docker-compose.yml logs -f

# Ver logs de un servicio específico
docker-compose -f docker/docker-compose.yml logs -f api

# Detener todos los servicios
docker-compose -f docker/docker-compose.yml down

# Detener y eliminar volúmenes
docker-compose -f docker/docker-compose.yml down -v
```

### 4.3. Gestión de Contenedores

```powershell
# Listar contenedores en ejecución
docker ps

# Ver logs de un contenedor
docker logs mlops-api
docker logs -f mlops-dashboard  # Modo follow

# Entrar a un contenedor (debugging)
docker exec -it mlops-api /bin/bash

# Ver uso de recursos
docker stats

# Reiniciar un servicio
docker-compose -f docker/docker-compose.yml restart api

# Reconstruir y reiniciar
docker-compose -f docker/docker-compose.yml up -d --build
```

---

## 5. Scripts de Inicio

### 5.1. `docker-start.sh` (Linux/Mac)

```bash
#!/bin/bash
# Script de inicio para Linux/Mac

echo "🐳 Iniciando servicios MLOps con Docker..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Navegar a la carpeta del proyecto
cd "$(dirname "$0")/../.."

# Construir imágenes
echo "📦 Construyendo imágenes..."
docker-compose -f docker/docker-compose.yml build

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose -f docker/docker-compose.yml up -d

# Verificar estado
echo "✅ Verificando estado de servicios..."
docker-compose -f docker/docker-compose.yml ps

echo ""
echo "🎉 Servicios iniciados exitosamente!"
echo ""
echo "📍 URLs de acceso:"
echo "   API:       http://localhost:5000"
echo "   Dashboard: http://localhost:8501"
echo "   Frontend:  http://localhost:3000"
echo ""
echo "📊 Ver logs: docker-compose -f docker/docker-compose.yml logs -f"
echo "🛑 Detener:  docker-compose -f docker/docker-compose.yml down"
```

**Uso:**
```bash
chmod +x docker/scripts/docker-start.sh
./docker/scripts/docker-start.sh
```

---

### 5.2. `docker-start.bat` (Windows)

```batch
@echo off
REM Script de inicio para Windows

echo 🐳 Iniciando servicios MLOps con Docker...

REM Verificar que Docker esté instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado
    exit /b 1
)

REM Navegar a la carpeta del proyecto
cd /d "%~dp0..\.."

REM Construir imágenes
echo 📦 Construyendo imágenes...
docker-compose -f docker\docker-compose.yml build

REM Iniciar servicios
echo 🚀 Iniciando servicios...
docker-compose -f docker\docker-compose.yml up -d

REM Verificar estado
echo ✅ Verificando estado de servicios...
docker-compose -f docker\docker-compose.yml ps

echo.
echo 🎉 Servicios iniciados exitosamente!
echo.
echo 📍 URLs de acceso:
echo    API:       http://localhost:5000
echo    Dashboard: http://localhost:8501
echo    Frontend:  http://localhost:3000
echo.
echo 📊 Ver logs: docker-compose -f docker\docker-compose.yml logs -f
echo 🛑 Detener:  docker-compose -f docker\docker-compose.yml down

pause
```

**Uso:**
```powershell
.\docker\scripts\docker-start.bat
```

---

## 6. Configuración Avanzada

### 6.1. Variables de Entorno

Crear archivo `.env` en la raíz:

```env
# API Configuration
FLASK_ENV=production
API_PORT=5000
LOG_LEVEL=INFO

# Dashboard Configuration
STREAMLIT_PORT=8501
STREAMLIT_THEME=light

# Model Configuration
MODEL_PATH=models/best_model.pkl
PREPROCESSOR_PATH=models/preprocessor.pkl

# Monitoring
PSI_THRESHOLD=0.2
DRIFT_CHECK_INTERVAL=3600
```

**Usar en docker-compose.yml:**
```yaml
services:
  api:
    env_file:
      - .env
    environment:
      - FLASK_ENV=${FLASK_ENV}
      - API_PORT=${API_PORT}
```

### 6.2. Volúmenes Persistentes

**Para no perder datos:**
```yaml
volumes:
  # Persistir modelos
  - ./models:/app/models:ro  # read-only

  # Persistir datos
  - ./data:/app/data

  # Persistir logs
  - ./logs:/app/logs
```

---

## 7. Optimización de Imágenes

### 7.1. Multi-stage Build

**Reducir tamaño de imagen:**
```dockerfile
# Stage 1: Builder
FROM python:3.10 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY mlops_pipeline/ ./mlops_pipeline/
COPY models/ ./models/

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "-m", "mlops_pipeline.src.model_deploy"]
```

**Beneficio:** Imagen final más pequeña (~200MB vs ~500MB)

### 7.2. .dockerignore

Crear archivo `.dockerignore` en la raíz:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
Proyecto-venv/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Data (copiar solo lo necesario)
data/raw/*.csv
data/processed/*.csv

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temp
tmp/
temp/
```

---

## 8. Despliegue en Cloud

### 8.1. AWS ECS (Elastic Container Service)

```powershell
# 1. Autenticar con ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# 2. Tag de imagen
docker tag mlops-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/mlops-api:latest

# 3. Push a ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/mlops-api:latest

# 4. Desplegar en ECS
aws ecs update-service --cluster mlops-cluster --service mlops-api --force-new-deployment
```

### 8.2. Azure Container Instances

```powershell
# 1. Login
az acr login --name <registry-name>

# 2. Tag
docker tag mlops-api:latest <registry-name>.azurecr.io/mlops-api:latest

# 3. Push
docker push <registry-name>.azurecr.io/mlops-api:latest

# 4. Deploy
az container create --resource-group mlops-rg --name mlops-api --image <registry-name>.azurecr.io/mlops-api:latest --cpu 2 --memory 4 --port 5000
```

### 8.3. Google Cloud Run

```powershell
# 1. Tag para GCR
docker tag mlops-api:latest gcr.io/<project-id>/mlops-api:latest

# 2. Push
docker push gcr.io/<project-id>/mlops-api:latest

# 3. Deploy
gcloud run deploy mlops-api --image gcr.io/<project-id>/mlops-api:latest --platform managed --region us-central1 --allow-unauthenticated
```

---

## 9. Monitoring de Contenedores

### 9.1. Health Checks

**Verificar salud de contenedores:**
```powershell
# Docker Compose health status
docker-compose -f docker/docker-compose.yml ps

# Inspeccionar health check
docker inspect --format='{{json .State.Health}}' mlops-api
```

### 9.2. Logs Centralizados

**Configurar logging driver:**
```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 9.3. Métricas con Prometheus

**Agregar exportador:**
```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

---

## 10. Troubleshooting

### Problema: "Cannot connect to the Docker daemon"
**Solución:** Iniciar Docker Desktop.

### Problema: "Port already in use"
**Solución:**
```powershell
# Encontrar proceso
netstat -ano | findstr :5000

# Matar proceso
taskkill /PID <PID> /F

# O cambiar puerto en docker-compose.yml
```

### Problema: "Container exits immediately"
**Solución:**
```powershell
# Ver logs
docker logs mlops-api

# Ver últimas líneas
docker logs --tail 50 mlops-api

# Ejecutar en modo interactivo
docker run -it mlops-api:latest /bin/bash
```

### Problema: "Out of disk space"
**Solución:**
```powershell
# Limpiar imágenes no usadas
docker image prune -a

# Limpiar todo
docker system prune -a --volumes
```

---

## 11. Seguridad

### 11.1. Buenas Prácticas

- [ ] No incluir secrets en Dockerfiles
- [ ] Usar variables de entorno para configuración
- [ ] Ejecutar como usuario no-root
- [ ] Escanear imágenes con herramientas de seguridad
- [ ] Mantener imágenes base actualizadas
- [ ] Usar imágenes oficiales verificadas

### 11.2. Escaneo de Vulnerabilidades

```powershell
# Con Docker Scout
docker scout cves mlops-api:latest

# Con Trivy
trivy image mlops-api:latest
```

---

## 12. Contacto

Para preguntas sobre Docker y containerización, referirse al README principal.

**Documentación relacionada:**
- [README Deployment](../docs/README_DEPLOYMENT.md)
- [README Principal](../docs/README_PRINCIPAL.md)
- [Docker Guide](../docs/docker/DOCKER_GUIDE.md)
