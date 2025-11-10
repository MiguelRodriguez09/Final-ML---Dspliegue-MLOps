# 🚀 REFERENCIA RÁPIDA - DOCKER

## ⚡ Comandos Más Usados

### Inicio y Detención
```bash
docker-compose up -d          # Iniciar servicios
docker-compose down           # Detener servicios
docker-compose restart        # Reiniciar servicios
docker-compose ps             # Ver estado
```

### Logs y Debugging
```bash
docker-compose logs -f                    # Ver todos los logs
docker-compose logs -f api                # Logs de API
docker-compose logs -f dashboard          # Logs de Dashboard
docker-compose logs --tail=100 -f         # Últimas 100 líneas
docker-compose exec api /bin/bash         # Shell en API
docker-compose exec dashboard /bin/bash   # Shell en Dashboard
```

### Build y Reconstrucción
```bash
docker-compose build                  # Construir imágenes
docker-compose build --no-cache       # Construir sin cache
docker-compose up -d --build          # Reconstruir y reiniciar
```

### Limpieza
```bash
docker-compose down                   # Detener y remover contenedores
docker-compose down -v                # + Remover volúmenes
docker-compose down -v --rmi all      # + Remover imágenes
docker system prune -af               # Limpiar todo Docker
```

---

## 🧪 Testing

### Probar API
```bash
# Health check
curl http://localhost:5000/

# Info del modelo
curl http://localhost:5000/model-info

# Predicción
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"CreditScore":619,"Geography":"France","Gender":"Female","Age":42,"Tenure":2,"Balance":0,"NumOfProducts":1,"HasCrCard":1,"IsActiveMember":1,"EstimatedSalary":101348.88}'
```

### Probar Dashboard
```bash
curl http://localhost:8501/_stcore/health
```

---

## 🔧 Troubleshooting

### Puerto en uso
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "5001:5000"  # Host:Container
```

### Ver logs de error
```bash
docker-compose logs api | grep ERROR
docker logs mlops-api --tail=50
```

### Reiniciar desde cero
```bash
docker-compose down -v --rmi all
docker-compose build --no-cache
docker-compose up -d
```

### Contenedor no inicia
```bash
docker logs mlops-api
docker inspect mlops-api
docker-compose logs -f api
```

---

## 📊 Monitoreo

```bash
# Ver uso de recursos
docker stats

# Ver específico
docker stats mlops-api mlops-dashboard

# Health status
docker inspect --format='{{.State.Health.Status}}' mlops-api
```

---

## 🎯 Makefile (si está disponible)

```bash
make help          # Ver todos los comandos
make build         # Construir imágenes
make up            # Iniciar servicios
make down          # Detener servicios
make logs          # Ver logs
make logs-api      # Logs de API
make logs-dashboard # Logs de Dashboard
make restart       # Reiniciar
make clean         # Limpiar todo
make rebuild       # Reconstruir todo
make test-api      # Probar API
make health        # Ver salud
make stats         # Ver recursos
```

---

## 🌐 URLs

- **API**: http://localhost:5000
- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:5000/model-info
- **Health Check**: http://localhost:5000/

---

## 📝 Variables de Entorno

Crear `.env` basado en `.env.example`:
```bash
FLASK_ENV=production
PORT=5000
STREAMLIT_SERVER_PORT=8501
```

---

## 🔄 Desarrollo vs Producción

### Desarrollo (con hot-reload)
```bash
docker-compose -f docker-compose.dev.yml up
```

### Producción
```bash
docker-compose up -d
```

---

## 📦 Archivos Importantes

- `Dockerfile` - Imagen de API
- `Dockerfile.streamlit` - Imagen de Dashboard
- `docker-compose.yml` - Producción
- `docker-compose.dev.yml` - Desarrollo
- `.dockerignore` - Exclusiones
- `Makefile` - Comandos útiles

---

## 🆘 Ayuda Rápida

1. **Problema de puertos**: Cambiar en `docker-compose.yml`
2. **Artefactos faltantes**: Ejecutar `python mlops_pipeline/src/model_training_evaluation.py`
3. **Error de build**: `docker-compose build --no-cache`
4. **Logs con errores**: `docker-compose logs -f api`
5. **Reiniciar todo**: `docker-compose down && docker-compose up -d`

---

## 📚 Documentación Completa

- **DOCKER_README.md** - Inicio rápido (¡EMPIEZA AQUÍ!)
- **DOCKER_GUIDE.md** - Guía exhaustiva
- **DOCKER_SUMMARY.md** - Resumen técnico

---

## ✅ Checklist

- [ ] Docker instalado
- [ ] Artefactos generados
- [ ] `docker-compose build` exitoso
- [ ] `docker-compose up -d` ejecutado
- [ ] API responde en :5000
- [ ] Dashboard en :8501
- [ ] Logs sin errores

---

**Proyecto:** Final-ML---Dspliegue-MLOps  
**Versión:** 1.0  
**Fecha:** Noviembre 2025
