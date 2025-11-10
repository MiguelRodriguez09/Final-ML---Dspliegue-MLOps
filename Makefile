# ============================================
# MLOps Pipeline - Makefile
# ============================================
# Comandos útiles para gestionar Docker
# ============================================

.PHONY: help build up down restart logs clean test shell

# Variables
PROJECT_NAME=mlops-pipeline
DOCKER_COMPOSE=docker-compose
DOCKER=docker

help: ## Mostrar ayuda
	@echo "MLOps Pipeline - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir las imágenes Docker
	@echo "🔨 Construyendo imágenes Docker..."
	$(DOCKER_COMPOSE) build --no-cache

build-api: ## Construir solo la imagen de la API
	@echo "🔨 Construyendo imagen de API..."
	$(DOCKER) build -t $(PROJECT_NAME)-api:latest -f Dockerfile .

build-dashboard: ## Construir solo la imagen del dashboard
	@echo "🔨 Construyendo imagen de Dashboard..."
	$(DOCKER) build -t $(PROJECT_NAME)-dashboard:latest -f Dockerfile.streamlit .

up: ## Iniciar los servicios
	@echo "🚀 Iniciando servicios..."
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Servicios iniciados!"
	@echo "📊 API disponible en: http://localhost:5000"
	@echo "📈 Dashboard disponible en: http://localhost:8501"

down: ## Detener los servicios
	@echo "🛑 Deteniendo servicios..."
	$(DOCKER_COMPOSE) down

restart: ## Reiniciar los servicios
	@echo "🔄 Reiniciando servicios..."
	$(DOCKER_COMPOSE) restart

logs: ## Ver logs de todos los servicios
	$(DOCKER_COMPOSE) logs -f

logs-api: ## Ver logs de la API
	$(DOCKER_COMPOSE) logs -f api

logs-dashboard: ## Ver logs del dashboard
	$(DOCKER_COMPOSE) logs -f dashboard

ps: ## Ver estado de los servicios
	$(DOCKER_COMPOSE) ps

shell-api: ## Abrir shell en el contenedor de la API
	$(DOCKER_COMPOSE) exec api /bin/bash

shell-dashboard: ## Abrir shell en el contenedor del dashboard
	$(DOCKER_COMPOSE) exec dashboard /bin/bash

test-api: ## Probar el endpoint de la API
	@echo "🧪 Probando API..."
	@curl -X GET http://localhost:5000/ || echo "❌ API no responde"
	@curl -X GET http://localhost:5000/model-info || echo "❌ Model-info no responde"

test-dashboard: ## Probar el dashboard
	@echo "🧪 Probando Dashboard..."
	@curl -f http://localhost:8501/_stcore/health || echo "❌ Dashboard no responde"

health: ## Verificar salud de los servicios
	@echo "🏥 Verificando salud de servicios..."
	@echo "API:"
	@$(DOCKER) inspect --format='{{.State.Health.Status}}' mlops-api 2>/dev/null || echo "No iniciado"
	@echo "Dashboard:"
	@$(DOCKER) inspect --format='{{.State.Health.Status}}' mlops-dashboard 2>/dev/null || echo "No iniciado"

clean: ## Limpiar contenedores, imágenes y volúmenes
	@echo "🧹 Limpiando recursos Docker..."
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans
	@echo "✅ Limpieza completada"

prune: ## Limpiar todo el sistema Docker (usar con precaución)
	@echo "⚠️  Limpiando sistema Docker completo..."
	$(DOCKER) system prune -af --volumes

rebuild: clean build up ## Reconstruir y reiniciar todo

stats: ## Ver estadísticas de uso de recursos
	$(DOCKER) stats --no-stream mlops-api mlops-dashboard

networks: ## Ver redes de Docker
	$(DOCKER) network ls | grep mlops

volumes: ## Ver volúmenes de Docker
	$(DOCKER) volume ls | grep mlops

# Comandos de desarrollo
dev: ## Modo desarrollo (con hot-reload)
	@echo "🛠️  Iniciando en modo desarrollo..."
	$(DOCKER_COMPOSE) up

prod: build up ## Modo producción
	@echo "🏭 Iniciando en modo producción..."

# Backup y restore
backup: ## Backup de artefactos del modelo
	@echo "💾 Creando backup..."
	@mkdir -p backups
	@tar -czf backups/model-artifacts-$$(date +%Y%m%d-%H%M%S).tar.gz *.pkl *.json *.csv
	@echo "✅ Backup creado en backups/"

# Default target
.DEFAULT_GOAL := help
