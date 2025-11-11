#!/bin/bash
# ============================================
# MLOps Pipeline - Docker Start Script
# ============================================
# Script para iniciar los servicios Docker
# Uso: ./docker-start.sh [api|dashboard|all]
# ============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo "============================================"
echo "   MLOps Pipeline - Docker Deployment"
echo "============================================"
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Por favor, instala Docker Compose primero."
    exit 1
fi

# Verificar que los artefactos existen
print_info "Verificando artefactos del modelo..."
if [ ! -f "best_model.pkl" ] || [ ! -f "preprocessor.pkl" ]; then
    print_warning "Artefactos del modelo no encontrados."
    print_info "Ejecuta el pipeline de entrenamiento primero:"
    print_info "  python mlops_pipeline/src/model_training_evaluation.py"
fi

# Determinar qué servicio iniciar
SERVICE=${1:-all}

case $SERVICE in
    api)
        print_info "Construyendo imagen de la API..."
        docker build -t mlops-api:latest -f Dockerfile .
        print_success "Imagen de API construida"
        
        print_info "Iniciando servicio de API..."
        docker run -d \
            --name mlops-api \
            -p 5000:5000 \
            -v "$(pwd)/best_model.pkl:/app/best_model.pkl:ro" \
            -v "$(pwd)/preprocessor.pkl:/app/preprocessor.pkl:ro" \
            -v "$(pwd)/model_metadata.json:/app/model_metadata.json:ro" \
            -v "$(pwd)/feature_engineering_metadata.json:/app/feature_engineering_metadata.json:ro" \
            mlops-api:latest
        
        print_success "API iniciada en http://localhost:5000"
        ;;
    
    dashboard)
        print_info "Construyendo imagen del Dashboard..."
        docker build -t mlops-dashboard:latest -f Dockerfile.streamlit .
        print_success "Imagen de Dashboard construida"
        
        print_info "Iniciando servicio de Dashboard..."
        docker run -d \
            --name mlops-dashboard \
            -p 8501:8501 \
            -v "$(pwd)/train_data.csv:/app/train_data.csv:ro" \
            -v "$(pwd)/test_data.csv:/app/test_data.csv:ro" \
            -v "$(pwd)/drift_report.json:/app/drift_report.json:ro" \
            -v "$(pwd)/model_metadata.json:/app/model_metadata.json:ro" \
            mlops-dashboard:latest
        
        print_success "Dashboard iniciado en http://localhost:8501"
        ;;
    
    all)
        print_info "Construyendo todas las imágenes..."
        docker-compose build
        print_success "Imágenes construidas"
        
        print_info "Iniciando todos los servicios..."
        docker-compose up -d
        print_success "Servicios iniciados"
        
        echo ""
        print_success "🎉 Deployment completado!"
        echo ""
        echo "📊 Servicios disponibles:"
        echo "  • API:       http://localhost:5000"
        echo "  • Dashboard: http://localhost:8501"
        echo ""
        echo "📝 Comandos útiles:"
        echo "  • Ver logs:        docker-compose logs -f"
        echo "  • Detener:         docker-compose down"
        echo "  • Ver estado:      docker-compose ps"
        echo ""
        ;;
    
    *)
        print_error "Servicio desconocido: $SERVICE"
        echo "Uso: $0 [api|dashboard|all]"
        exit 1
        ;;
esac

# Esperar a que los servicios estén listos
print_info "Esperando a que los servicios estén listos..."
sleep 5

# Health check
if [ "$SERVICE" == "api" ] || [ "$SERVICE" == "all" ]; then
    print_info "Verificando API..."
    if curl -f http://localhost:5000/ &> /dev/null; then
        print_success "API respondiendo correctamente"
    else
        print_warning "API aún no está lista. Espera unos segundos más."
    fi
fi

if [ "$SERVICE" == "dashboard" ] || [ "$SERVICE" == "all" ]; then
    print_info "Verificando Dashboard..."
    if curl -f http://localhost:8501/_stcore/health &> /dev/null; then
        print_success "Dashboard respondiendo correctamente"
    else
        print_warning "Dashboard aún no está listo. Espera unos segundos más."
    fi
fi

print_success "Deployment completado! 🚀"
