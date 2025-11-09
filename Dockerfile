# Dockerfile para MLOps Pipeline
# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY mlops_pipeline/ ./mlops_pipeline/
COPY Churn_Modelling.csv .

# Exponer el puerto de la API
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=mlops_pipeline/src/model_deploy.py

# Comando para ejecutar la aplicación
CMD ["python", "mlops_pipeline/src/model_deploy.py"]
