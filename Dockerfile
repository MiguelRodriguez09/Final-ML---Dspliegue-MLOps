# ============================================
# MLOps Pipeline - Dockerfile
# ============================================
# Multi-stage build para optimizar tamaño
# Soporta tanto API Flask como Streamlit
# ============================================

# Stage 1: Builder
FROM python:3.10-slim AS builder

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio para dependencias
WORKDIR /install

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias en un directorio específico
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

# Metadata
LABEL maintainer="MiguelRodriguez09"
LABEL description="MLOps Pipeline - API & Monitoring"
LABEL version="1.0"

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 mlops && \
    mkdir -p /app && \
    chown -R mlops:mlops /app

# Copiar dependencias desde builder
COPY --from=builder /install /usr/local

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código de la aplicación
COPY --chown=mlops:mlops mlops_pipeline/ mlops_pipeline/
COPY --chown=mlops:mlops requirements.txt .

# Copiar artefactos del modelo (copiado durante el build, si faltan usar volúmenes)
COPY --chown=mlops:mlops best_model.pkl preprocessor.pkl ./ 
COPY --chown=mlops:mlops model_metadata.json feature_engineering_metadata.json eda_metadata.json ./
COPY --chown=mlops:mlops train_data.csv test_data.csv ./

# Exponer puertos
EXPOSE 5000 8501

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=mlops_pipeline/src/model_deploy.py \
    PYTHONPATH=/app \
    PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Cambiar a usuario no-root
USER mlops

# Comando de inicio (puede ser sobreescrito)
CMD ["python", "mlops_pipeline/src/model_deploy.py"]
