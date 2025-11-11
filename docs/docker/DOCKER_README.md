# ============================================
# MLOps Pipeline - README Docker
# ============================================

## 🐳 Contenerización Docker - Inicio Rápido

### Archivos Creados

Este proyecto incluye una configuración completa de Docker con los siguientes archivos:

```
📦 Archivos Docker
├── Dockerfile                    # Imagen principal (Flask API)
├── Dockerfile.streamlit          # Imagen del Dashboard
├── docker-compose.yml            # Orquestación de servicios
├── .dockerignore                 # Exclusiones del build
├── Makefile                      # Comandos útiles
├── docker-start.sh              # Script de inicio (Linux/Mac)
├── docker-start.bat             # Script de inicio (Windows)
└── DOCKER_GUIDE.md              # Guía completa (LEE ESTO PRIMERO)
```

---

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Verificar requisitos

```bash
# Verificar Docker instalado
docker --version
docker-compose --version
```

### Paso 2: Construir imágenes

```bash
# Construir todas las imágenes
docker-compose build
```

### Paso 3: Iniciar servicios

```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar que están corriendo
docker-compose ps
```

### ✅ Listo!

- **API Flask**: http://localhost:5000
- **Dashboard Streamlit**: http://localhost:8501

---

## 📋 Comandos Principales

### Gestión Básica

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Ver estado
docker-compose ps
```

### Con Makefile (Recomendado)

```bash
# Ver todos los comandos disponibles
make help

# Construir imágenes
make build

# Iniciar servicios
make up

# Ver logs
make logs

# Detener servicios
make down

# Limpieza completa
make clean
```

### Con Scripts

#### Windows
```cmd
docker-start.bat all
```

#### Linux/Mac
```bash
chmod +x docker-start.sh
./docker-start.sh all
```

---

## 🧪 Probar los Servicios

### Probar API

```bash
# Health check
curl http://localhost:5000/

# Información del modelo
curl http://localhost:5000/model-info

# Predicción
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
```

### Probar Dashboard

Abre en tu navegador: http://localhost:8501

---

## 🔧 Configuración

### Variables de Entorno

Puedes personalizar las variables en `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - PORT=5000
  - PYTHONUNBUFFERED=1
```

### Puertos

Por defecto:
- API: `5000:5000`
- Dashboard: `8501:8501`

Para cambiar el puerto del host:

```yaml
ports:
  - "5001:5000"  # API en puerto 5001
  - "8502:8501"  # Dashboard en puerto 8502
```

---

## 🐛 Troubleshooting

### Error: Puerto en uso

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "5001:5000"  # Usar puerto diferente
```

### Error: Artefactos no encontrados

```bash
# Ejecutar pipeline de entrenamiento primero
python mlops_pipeline/src/model_training_evaluation.py

# Verificar archivos
ls -la *.pkl *.json *.csv
```

### Ver logs de errores

```bash
# Ver logs de un servicio específico
docker-compose logs api
docker-compose logs dashboard

# Ver últimas 100 líneas
docker-compose logs --tail=100 -f
```

### Contenedor se detiene

```bash
# Ver logs del contenedor
docker logs mlops-api

# Ejecutar en modo interactivo para debugging
docker run -it mlops-api:latest /bin/bash
```

---

## 📊 Arquitectura

```
┌─────────────────────────────────────┐
│      Docker Compose Network          │
├─────────────────────────────────────┤
│                                      │
│  ┌──────────┐      ┌──────────┐    │
│  │   API    │      │Dashboard │    │
│  │ (Flask)  │◄────►│(Streamlit│    │
│  │Port: 5000│      │Port: 8501│    │
│  └──────────┘      └──────────┘    │
│       │                  │          │
│       └────────┬─────────┘          │
│                ▼                    │
│         [Shared Volumes]            │
│      - Model artifacts              │
│      - Data files                   │
│      - Metadata                     │
└─────────────────────────────────────┘
```

---

## 📚 Documentación Completa

Para información detallada, consulta:

- **DOCKER_GUIDE.md** - Guía completa de Docker
  - Configuración avanzada
  - Deployment a producción
  - Mejores prácticas
  - Troubleshooting detallado

---

## ✅ Checklist de Deployment

- [ ] Docker instalado y corriendo
- [ ] Artefactos del modelo generados
- [ ] Imágenes construidas (`docker-compose build`)
- [ ] Servicios iniciados (`docker-compose up -d`)
- [ ] API responde en http://localhost:5000
- [ ] Dashboard carga en http://localhost:8501
- [ ] Logs verificados sin errores críticos

---

## 🛠️ Mantenimiento

```bash
# Actualizar servicios
docker-compose pull
docker-compose up -d

# Backup de datos
make backup  # Si usas Makefile

# Ver uso de recursos
docker stats

# Limpiar recursos no usados
docker system prune
```

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa **DOCKER_GUIDE.md** (documentación completa)
2. Verifica logs: `docker-compose logs -f`
3. Consulta sección de Troubleshooting
4. Abre un issue en el repositorio

---

## 📝 Notas Importantes

### Seguridad
- Los contenedores corren con usuario no-root
- Health checks habilitados
- Recursos limitados en docker-compose.yml

### Performance
- Multi-stage builds para optimizar tamaño
- Cache de layers de Docker
- .dockerignore configurado

### Producción
Para deployment en producción, revisa:
- Configuración de SSL/TLS
- Secrets management
- Escalado horizontal
- Monitoreo y logging centralizado

---

**¡Todo listo para contenerizar! 🚀**

```bash
docker-compose up -d
```

---

**Documentación creada:** Noviembre 10, 2025  
**Versión:** 1.0  
**Proyecto:** Final-ML---Dspliegue-MLOps
