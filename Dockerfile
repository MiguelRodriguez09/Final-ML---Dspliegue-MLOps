# Usar imagen base de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY mlops_pipeline/ mlops_pipeline/
COPY *.pkl ./
COPY *.csv ./
COPY *.json ./

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=mlops_pipeline/src/model_deploy.py

# Comando de inicio
CMD ["python", "mlops_pipeline/src/model_deploy.py"]
