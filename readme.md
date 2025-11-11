# Proyecto Final: MLOps - Sistema de Predicción de Churn

## 1. Propósito

Este proyecto implementa un **pipeline completo de MLOps** para la predicción de churn de clientes bancarios. El sistema incluye desde el análisis exploratorio de datos hasta el despliegue y monitoreo continuo del modelo en producción, siguiendo las mejores prácticas de Machine Learning Operations.

### Características Principales:
- ✅ Pipeline automatizado de ML
- ✅ Análisis exploratorio de datos (EDA)
- ✅ Ingeniería de características con sklearn pipelines
- ✅ Entrenamiento y evaluación de múltiples modelos
- ✅ API REST para predicciones
- ✅ Monitoreo de data drift
- ✅ Dashboard interactivo con Streamlit
- ✅ Containerización con Docker

---

## 2. Estructura del Proyecto

```
Proyecto/
├── mlops_pipeline/
│   └── src/
│       ├── cargar_datos.ipynb              # Notebook: Carga y exploración inicial
│       ├── compresion_eda.ipynb            # Notebook: EDA completo
│       ├── ft_engineering.py               # Feature Engineering
│       ├── model_training_evaluation.py    # Entrenamiento y Evaluación
│       ├── model_deploy.py                 # API REST (Flask)
│       ├── model_monitoring.py             # Monitoreo de Drift
│       └── streamlit_app.py                # Dashboard de visualización
├── data/
│   ├── raw/                    # Datos originales
│   ├── processed/              # Datos procesados (train/test)
│   └── metadata/               # Metadatos y reportes
├── models/                     # Modelos entrenados y artifacts
├── frontend/                   # Interfaz web
├── docker/                     # Archivos Docker
├── docs/                       # Documentación adicional
├── reports/                    # Reportes y visualizaciones
├── requirements.txt            # Dependencias de Python
├── Makefile                    # Comandos automatizados
└── README.md                   # Este archivo
```

---

## 3. Instalación y Configuración

### 3.1. Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes)
- Git
- Docker (opcional, para despliegue en contenedores)

### 3.2. Configuración del Entorno Virtual

**En Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv Proyecto-venv

# Activar entorno virtual
.\Proyecto-venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

**En Linux/Mac:**
```bash
# Crear entorno virtual
python3 -m venv Proyecto-venv

# Activar entorno virtual
source Proyecto-venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3.3. Verificar Instalación
```powershell
# Verificar versión de Python
python --version

# Verificar paquetes instalados
pip list
```

---

## 4. Ejecución del Pipeline Completo

### 4.1. Pipeline Paso a Paso

**Paso 1: Análisis Exploratorio de Datos (EDA)**
```powershell
# Ejecutar notebooks de análisis (Jupyter)
jupyter notebook mlops_pipeline/src/compresion_eda.ipynb
```

**Paso 2: Feature Engineering**
```powershell
# Procesar características y crear datasets de train/test
python -m mlops_pipeline.src.ft_engineering
```

**Paso 3: Entrenamiento de Modelos**
```powershell
# Entrenar y evaluar múltiples modelos
python -m mlops_pipeline.src.model_training_evaluation
```

**Paso 4: Monitoreo de Drift**
```powershell
# Ejecutar análisis de drift
python -m mlops_pipeline.src.model_monitoring
```

**Paso 5: Despliegue de API**
```powershell
# Iniciar servidor Flask
python -m mlops_pipeline.src.model_deploy
```

**Paso 6: Dashboard de Monitoreo**
```powershell
# Iniciar aplicación Streamlit
streamlit run mlops_pipeline/src/streamlit_app.py
```

### 4.2. Ejecución Rápida con Makefile

Si tienes `make` instalado:
```powershell
# Ejecutar pipeline completo
make all

# O paso por paso
make feature-engineering
make train
make monitor
make deploy
make dashboard
```

---

## 5. Mapeo de Requisitos del Checklist

### 5.1. Estructura del Proyecto y Configuración

| Requisito del Checklist | Ubicación | Descripción |
|:---|:---|:---|
| **¿El proyecto tiene una estructura organizada?** | Carpeta raíz | Estructura modular con separación clara de responsabilidades |
| **¿Existe un archivo `requirements.txt`?** | `requirements.txt` | Lista completa de dependencias con versiones |
| **¿Se utiliza un entorno virtual?** | `Proyecto-venv/` | Entorno virtual Python para aislamiento de dependencias |
| **¿Hay documentación README?** | `README.md`, `docs/` | Documentación completa de instalación y uso |

### 5.2. Análisis de Datos (EDA)

| Requisito del Checklist | Archivo | Ubicación en Código |
|:---|:---|:---|
| **¿Se realiza un EDA completo?** | `compresion_eda.ipynb` | Todo el notebook |
| **¿Se identifican valores nulos?** | `compresion_eda.ipynb` | Secciones de análisis de calidad |
| **¿Se detectan outliers?** | `compresion_eda.ipynb` | Secciones de visualización (boxplots) |
| **¿Se analizan distribuciones?** | `compresion_eda.ipynb` | Histogramas y gráficos de distribución |
| **¿Se genera data_cleaned.csv?** | `compresion_eda.ipynb` | Al final del notebook → `data/processed/data_cleaned.csv` |

### 5.3. Ingeniería de Características

| Requisito del Checklist | Archivo | Función/Línea |
|:---|:---|:---|
| **¿Se usa ColumnTransformer?** | `ft_engineering.py` | `build_preprocessor()` (línea ~157) |
| **¿Se aplican pipelines de sklearn?** | `ft_engineering.py` | `build_preprocessor()` (línea ~157) |
| **¿Se procesan variables numéricas?** | `ft_engineering.py` | Pipeline `num_continuous`, `num_discrete` (línea ~168-189) |
| **¿Se procesan variables categóricas?** | `ft_engineering.py` | Pipeline `cat` con OneHotEncoder (línea ~192-201) |
| **¿Se guarda el preprocessor?** | `ft_engineering.py` | `save_preprocessor()` (línea ~243) |
| **¿Se genera train/test split?** | `ft_engineering.py` | `split_train_test()` (línea ~213) |
| **¿Se exportan train_data.csv y test_data.csv?** | `ft_engineering.py` | `save_processed_data()` (línea ~267) |
| **¿Se documenta metadata?** | `ft_engineering.py` | `save_metadata()` (línea ~297) |

### 5.4. Entrenamiento y Evaluación

| Requisito del Checklist | Archivo | Función/Línea |
|:---|:---|:---|
| **¿Se entrenan múltiples modelos?** | `model_training_evaluation.py` | `build_models()` (línea ~122) |
| **¿Se usa función build_model()?** | `model_training_evaluation.py` | `build_models()` (línea ~122) |
| **¿Se aplica cross-validation?** | `model_training_evaluation.py` | `train_with_cross_validation()` (línea ~159) |
| **¿Se guarda el mejor modelo?** | `model_training_evaluation.py` | `save_best_model()` (línea ~360) |
| **¿Se usa summarize_classification()?** | `model_training_evaluation.py` | `summarize_classification()` (línea ~256) |
| **¿Se comparan modelos con métricas?** | `model_training_evaluation.py` | `evaluate_model()` (línea ~202) |
| **¿Se generan gráficos (ROC, Confusion Matrix)?** | `model_training_evaluation.py` | `plot_roc_curves()` (línea ~393), `plot_confusion_matrices()` (línea ~444) |
| **¿Se justifica selección del modelo?** | `model_training_evaluation.py` | `select_best_model()` (línea ~282) + Comentarios |

### 5.5. Data Monitoring (Drift Detection)

| Requisito del Checklist | Archivo | Función/Línea |
|:---|:---|:---|
| **¿Se implementa monitoreo de drift?** | `model_monitoring.py` | Clase `DriftMonitor` (línea ~31) |
| **¿Se usa PSI (Population Stability Index)?** | `model_monitoring.py` | `calculate_psi()` (línea ~75) |
| **¿Se usa Kolmogorov-Smirnov test?** | `model_monitoring.py` | `detect_numerical_drift()` (línea ~159) |
| **¿Se genera drift_report.json?** | `model_monitoring.py` | `save_drift_report()` (línea ~383) |
| **¿Se generan alertas?** | `model_monitoring.py` | `generate_alerts()` (línea ~335) |
| **¿Se visualiza el drift?** | `streamlit_app.py` | Dashboard completo |

### 5.6. Despliegue (Deployment)

| Requisito del Checklist | Archivo | Función/Línea |
|:---|:---|:---|
| **¿Se crea una API REST?** | `model_deploy.py` | Flask app (línea ~30) |
| **¿Existe endpoint /predict?** | `model_deploy.py` | `@app.route('/predict')` (línea ~145) |
| **¿Se validan inputs?** | `model_deploy.py` | `validate_input_data()` (línea ~82) |
| **¿Se cargan artefactos (modelo + preprocessor)?** | `model_deploy.py` | `load_artifacts()` (línea ~41) |
| **¿Se proporciona health check?** | `model_deploy.py` | `@app.route('/')` (línea ~119) |
| **¿Existe interfaz web/frontend?** | `frontend/index.html` | Interfaz HTML + JavaScript |
| **¿Hay archivos Docker?** | `docker/Dockerfile` | Dockerfiles para containerización |

### 5.7. Documentación y Buenas Prácticas

| Requisito del Checklist | Ubicación | Notas |
|:---|:---|:---|
| **¿Código documentado con docstrings?** | Todos los archivos `.py` | Docstrings tipo Google en todas las funciones |
| **¿Se usa logging?** | Todos los módulos | `logging` configurado en cada módulo |
| **¿Código modular y reutilizable?** | `mlops_pipeline/src/` | Clases y funciones genéricas |
| **¿Existe documentación de deployment?** | `reports/deployment/` | Reportes de despliegue |

---

## 6. Endpoints de la API

### 6.1. Health Check
```http
GET http://localhost:5000/
```

**Respuesta:**
```json
{
  "status": "ok",
  "message": "MLOps API is running",
  "model_loaded": true
}
```

### 6.2. Predicción
```http
POST http://localhost:5000/predict
Content-Type: application/json

{
  "CreditScore": 619,
  "Geography": "France",
  "Gender": "Female",
  "Age": 42,
  "Tenure": 2,
  "Balance": 0.0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 101348.88
}
```

**Respuesta:**
```json
{
  "predictions": [1],
  "probabilities": [[0.25, 0.75]],
  "model_name": "Random Forest"
}
```

### 6.3. Información del Modelo
```http
GET http://localhost:5000/model-info
```

---

## 7. Dashboard de Monitoreo (Streamlit)

El dashboard proporciona:
- 📊 Visualización de métricas de drift
- 🚨 Alertas de data drift
- 📈 Gráficos interactivos
- 🔄 Análisis en tiempo real

**Acceso:** http://localhost:8501

---

## 8. Despliegue con Docker

### 8.1. Construcción de Imágenes
```powershell
# Construir imagen de la API
docker build -f docker/Dockerfile -t mlops-api:latest .

# Construir imagen del dashboard
docker build -f docker/Dockerfile.streamlit -t mlops-dashboard:latest .
```

### 8.2. Ejecución con Docker Compose
```powershell
# Iniciar todos los servicios
docker-compose -f docker/docker-compose.yml up -d

# Ver logs
docker-compose -f docker/docker-compose.yml logs -f

# Detener servicios
docker-compose -f docker/docker-compose.yml down
```

---

## 9. Testing y Validación

### 9.1. Ejecutar Tests
```powershell
# Tests del frontend
python frontend/test_frontend.py

# Tests de la API (si existen)
pytest tests/
```

---

## 10. Contribuciones y Desarrollo

### 10.1. Flujo de Trabajo
1. Crear una rama para nuevas características
2. Realizar cambios y commit
3. Ejecutar tests
4. Crear Pull Request

### 10.2. Estándares de Código
- Seguir PEP 8 para Python
- Documentar todas las funciones
- Usar type hints
- Logging adecuado

---

## 11. Contacto y Soporte

**Autor:** Miguel Rodriguez  
**Repositorio:** [Final-ML---Dspliegue-MLOps](https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps)  
**Branch:** dev

---

## 12. Licencia

Este proyecto es parte de un trabajo académico para la clase de Machine Learning.

---

## 13. Recursos Adicionales

- 📖 [Guía de Docker](docker/DOCKER_GUIDE.md)
- 🚀 [Quick Start](setup/QUICKSTART.md)
- 🔍 [Análisis y Refactorización](../ANALISIS_REFACTORIZACION.md)
- 🧪 [Guía de Pruebas](../GUIA_PRUEBAS.md)
