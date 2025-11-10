# 🐳 Guía de Contenerización Docker - MLOps Pipeline

Esta guía proporciona instrucciones completas para contenerizar y desplegar el proyecto MLOps Pipeline usando Docker.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Arquitectura de Contenedores](#arquitectura-de-contenedores)
3. [Archivos de Docker](#archivos-de-docker)
4. [Inicio Rápido](#inicio-rápido)
5. [Comandos Detallados](#comandos-detallados)
6. [Configuración Avanzada](#configuración-avanzada)
7. [Troubleshooting](#troubleshooting)
8. [Mejores Prácticas](#mejores-prácticas)

---

## 🔧 Requisitos Previos

### Software Necesario

1. **Docker Desktop** (Windows/Mac) o **Docker Engine** (Linux)
   - Descargar: https://www.docker.com/products/docker-desktop
   - Versión mínima: 20.10.0

2. **Docker Compose**
   - Incluido en Docker Desktop
   - Linux: `sudo apt-get install docker-compose`

3. **Artefactos del Modelo** (generados previamente)
   - `best_model.pkl`
   - `preprocessor.pkl`
   - `model_metadata.json`
   - `feature_engineering_metadata.json`
   - `train_data.csv`
   - `test_data.csv`

### Verificar Instalación

```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar que Docker está corriendo
docker ps
```

---

## 🏗️ Arquitectura de Contenedores

### Servicios

```
┌─────────────────────────────────────────────────┐
│              MLOps Pipeline                      │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────┐         ┌──────────────┐      │
│  │   API       │         │  Dashboard   │      │
│  │  (Flask)    │         │ (Streamlit)  │      │
│  │  Port: 5000 │         │  Port: 8501  │      │
│  └─────────────┘         └──────────────┘      │
│         │                        │              │
│         └────────┬───────────────┘              │
│                  │                              │
│         ┌────────▼────────┐                     │
│         │  mlops-network  │                     │
│         └─────────────────┘                     │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Puertos Expuestos

| Servicio   | Puerto | Descripción                    |
|------------|--------|--------------------------------|
| API        | 5000   | Endpoint REST para predicciones|
| Dashboard  | 8501   | Interfaz Streamlit de monitoreo|

---

## 📁 Archivos de Docker

### Archivos Creados

```
Proyecto/
├── Dockerfile                 # Imagen principal (API Flask)
├── Dockerfile.streamlit       # Imagen para Dashboard
├── docker-compose.yml         # Orquestación de servicios
├── .dockerignore             # Archivos a excluir del build
├── Makefile                  # Comandos útiles
├── docker-start.sh           # Script de inicio (Linux/Mac)
├── docker-start.bat          # Script de inicio (Windows)
└── DOCKER_GUIDE.md           # Esta guía
```

### Descripción de Archivos

#### `Dockerfile`
- Imagen multi-stage para optimizar tamaño
- Usuario no-root para seguridad
- Health checks incluidos
- Optimizado para producción

#### `Dockerfile.streamlit`
- Imagen específica para el dashboard
- Configuración de Streamlit
- Puerto 8501 expuesto

#### `docker-compose.yml`
- Orquestación de ambos servicios
- Configuración de redes
- Volúmenes para persistencia
- Límites de recursos

---

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

```bash
# 1. Construir las imágenes
docker-compose build

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Verificar que están corriendo
docker-compose ps

# 4. Ver logs
docker-compose logs -f
```

**Servicios disponibles:**
- API: http://localhost:5000
- Dashboard: http://localhost:8501

### Opción 2: Scripts de Inicio

#### Windows (PowerShell)
```powershell
.\docker-start.bat all
```

#### Linux/Mac
```bash
chmod +x docker-start.sh
./docker-start.sh all
```

### Opción 3: Makefile

```bash
# Ver comandos disponibles
make help

# Construir y iniciar
make build
make up

# O todo en uno
make prod
```

### Opción 4: Docker Manual

#### Solo API
```bash
# Construir
docker build -t mlops-api:latest -f Dockerfile .

# Ejecutar
docker run -d \
  --name mlops-api \
  -p 5000:5000 \
  -v $(pwd)/best_model.pkl:/app/best_model.pkl:ro \
  -v $(pwd)/preprocessor.pkl:/app/preprocessor.pkl:ro \
  mlops-api:latest
```

#### Solo Dashboard
```bash
# Construir
docker build -t mlops-dashboard:latest -f Dockerfile.streamlit .

# Ejecutar
docker run -d \
  --name mlops-dashboard \
  -p 8501:8501 \
  -v $(pwd)/drift_report.json:/app/drift_report.json:ro \
  mlops-dashboard:latest
```

---

## 📚 Comandos Detallados

### Gestión de Servicios

```bash
# Iniciar servicios en modo detached
docker-compose up -d

# Iniciar servicios en foreground (ver logs en tiempo real)
docker-compose up

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver estado de servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f api
docker-compose logs -f dashboard
```

### Construcción de Imágenes

```bash
# Construir todas las imágenes
docker-compose build

# Construir sin cache
docker-compose build --no-cache

# Construir una imagen específica
docker-compose build api
docker-compose build dashboard

# Construir imagen individual
docker build -t mlops-api:latest -f Dockerfile .
docker build -t mlops-dashboard:latest -f Dockerfile.streamlit .
```

### Debugging

```bash
# Abrir shell en contenedor de API
docker-compose exec api /bin/bash

# Abrir shell en contenedor de Dashboard
docker-compose exec dashboard /bin/bash

# Ejecutar comando en contenedor
docker-compose exec api python --version
docker-compose exec api ls -la /app

# Inspeccionar logs en tiempo real
docker-compose logs --tail=100 -f api
```

### Gestión de Recursos

```bash
# Ver uso de recursos
docker stats mlops-api mlops-dashboard

# Ver información del contenedor
docker inspect mlops-api

# Ver redes
docker network ls

# Ver volúmenes
docker volume ls
```

### Limpieza

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar contenedores y volúmenes
docker-compose down -v

# Eliminar contenedores, volúmenes e imágenes
docker-compose down -v --rmi all

# Limpiar sistema completo (¡CUIDADO!)
docker system prune -af --volumes
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_APP=mlops_pipeline/src/model_deploy.py
PORT=5000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Model Configuration
MODEL_PATH=/app/best_model.pkl
PREPROCESSOR_PATH=/app/preprocessor.pkl

# Logging
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

Luego referenciar en `docker-compose.yml`:

```yaml
services:
  api:
    env_file:
      - .env
```

### Volúmenes Persistentes

Para mantener datos entre reinicios:

```yaml
volumes:
  model-data:
    driver: local

services:
  api:
    volumes:
      - model-data:/app/models
```

### Escalado Horizontal

```bash
# Escalar el servicio de API a 3 réplicas
docker-compose up -d --scale api=3
```

### Health Checks Personalizados

Ya incluidos en los Dockerfiles:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1
```

### Límites de Recursos

Configurar en `docker-compose.yml`:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 🧪 Testing

### Probar API

```bash
# Health check
curl http://localhost:5000/

# Información del modelo
curl http://localhost:5000/model-info

# Predicción individual
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "CreditScore": 619,
    "Geography": "France",
    "Gender": "Female",
    "Age": 42,
    "Tenure": 2,
    "Balance": 0,
    "NumOfProducts": 1,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": 101348.88
  }'

# Predicción por lotes
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '[
    {"CreditScore": 619, "Geography": "France", "Gender": "Female", ...},
    {"CreditScore": 608, "Geography": "Spain", "Gender": "Male", ...}
  ]'
```

### Probar Dashboard

```bash
# Health check
curl http://localhost:8501/_stcore/health

# Abrir en navegador
# Windows
start http://localhost:8501

# Linux
xdg-open http://localhost:8501

# Mac
open http://localhost:8501
```

---

## 🔍 Troubleshooting

### Problema: Puerto ya en uso

**Error:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use
```

**Solución:**
```bash
# Encontrar proceso usando el puerto
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # Linux/Mac

# Matar proceso
kill -9 <PID>                  # Linux/Mac
taskkill /PID <PID> /F        # Windows

# O cambiar puerto en docker-compose.yml
ports:
  - "5001:5000"  # Host:Container
```

### Problema: Artefactos no encontrados

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'best_model.pkl'
```

**Solución:**
```bash
# Ejecutar pipeline de entrenamiento primero
python mlops_pipeline/src/model_training_evaluation.py

# Verificar que los archivos existen
ls -la *.pkl *.json *.csv
```

### Problema: Imagen muy grande

**Solución:**
```bash
# Ver tamaño de imagen
docker images mlops-api

# Optimizar .dockerignore
# Usar multi-stage builds (ya implementado)
# Limpiar cache de pip
RUN pip install --no-cache-dir -r requirements.txt
```

### Problema: Contenedor se detiene inmediatamente

**Solución:**
```bash
# Ver logs del contenedor
docker logs mlops-api

# Ejecutar en modo interactivo para debugging
docker run -it mlops-api:latest /bin/bash

# Verificar health check
docker inspect --format='{{.State.Health.Status}}' mlops-api
```

### Problema: Error de permisos

**Error:**
```
PermissionError: [Errno 13] Permission denied: '/app/models'
```

**Solución:**
```bash
# Verificar ownership en Dockerfile
RUN chown -R mlops:mlops /app

# O ejecutar como root (no recomendado para producción)
USER root
```

---

## ✅ Mejores Prácticas

### Seguridad

1. **No usar usuario root**
   ```dockerfile
   RUN useradd -m -u 1000 mlops
   USER mlops
   ```

2. **No incluir secretos en imagen**
   - Usar variables de entorno
   - Usar Docker secrets
   - Usar archivos .env (no commitear)

3. **Actualizar imagen base regularmente**
   ```dockerfile
   FROM python:3.10-slim
   ```

### Performance

1. **Multi-stage builds** (ya implementado)
2. **Cache de layers de Docker**
3. **Minimizar número de layers**
4. **Usar .dockerignore** (ya implementado)

### Producción

1. **Health checks** (ya implementado)
2. **Logging centralizado**
3. **Monitoreo de métricas**
4. **Backup de datos**
5. **CI/CD pipeline**

### Mantenimiento

```bash
# Backup regular de artefactos
make backup

# Actualizar imágenes
docker-compose pull
docker-compose up -d

# Monitorear logs
docker-compose logs -f --tail=100

# Revisar uso de recursos
docker stats
```

---

## 📊 Monitoreo y Logging

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker-compose logs -f

# Últimas 100 líneas
docker-compose logs --tail=100 -f

# Solo errores
docker-compose logs | grep ERROR
```

### Métricas de Recursos

```bash
# Ver uso de CPU, memoria, red
docker stats

# Exportar a archivo
docker stats --no-stream > stats.txt
```

---

## 🚢 Deployment a Producción

### Docker Hub

```bash
# Login
docker login

# Tag imagen
docker tag mlops-api:latest username/mlops-api:v1.0

# Push
docker push username/mlops-api:v1.0
```

### Cloud Platforms

#### AWS ECS
```bash
# Ver guía oficial de AWS ECS
# https://docs.aws.amazon.com/ecs/
```

#### Google Cloud Run
```bash
# Deploy a Cloud Run
gcloud run deploy mlops-api \
  --image gcr.io/project-id/mlops-api:latest \
  --platform managed
```

#### Azure Container Instances
```bash
# Deploy a Azure
az container create \
  --resource-group myResourceGroup \
  --name mlops-api \
  --image myregistry.azurecr.io/mlops-api:latest
```

---

## 📝 Checklist de Deployment

- [ ] Artefactos del modelo generados
- [ ] Docker y Docker Compose instalados
- [ ] .dockerignore configurado
- [ ] Variables de entorno configuradas
- [ ] Imágenes construidas exitosamente
- [ ] Health checks funcionando
- [ ] API responde correctamente
- [ ] Dashboard carga correctamente
- [ ] Logs verificados sin errores
- [ ] Recursos monitoreados
- [ ] Backup de datos configurado

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisar logs: `docker-compose logs -f`
2. Verificar health checks: `docker ps`
3. Consultar esta guía
4. Revisar issues en el repositorio

---

## 📚 Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

---

**¡Deployment exitoso! 🎉**

Para comenzar, ejecuta:
```bash
docker-compose up -d
```
