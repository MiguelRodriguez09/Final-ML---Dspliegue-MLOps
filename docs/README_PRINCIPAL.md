# 📘 README PRINCIPAL - Proyecto MLOps: Predicción de Churn Bancario

## 📋 Información del Proyecto

- **Repositorio:** Final-ML---Dspliegue-MLOps
- **Branch:** dev
- **Owner:** MiguelRodriguez09
- **Propósito:** Sistema MLOps completo para predicción de churn bancario con monitoreo de drift, API REST y dashboard interactivo

---

## 🎯 Objetivo General

Este proyecto implementa un **pipeline MLOps end-to-end** que cubre:
1. **EDA (Exploratory Data Analysis)**: Análisis exploratorio de datos
2. **Feature Engineering**: Ingeniería de características con pipelines de sklearn
3. **Model Training**: Entrenamiento y evaluación de 4 modelos ML
4. **Model Deployment**: API REST con Flask para predicciones
5. **Model Monitoring**: Detección de drift de datos con Streamlit
6. **Containerization**: Docker y Docker Compose para deployment

---

## 🏗️ Arquitectura del Sistema

```
┌────────────────────────────────────────────────────────────────┐
│                      MLOPS PIPELINE                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  EDA & Data Processing                                      │
│      ├─ compresion_eda.ipynb                                   │
│      ├─ cargar_datos.ipynb                                     │
│      └─ Output: data/processed/data_cleaned.csv                │
│                                                                 │
│  2️⃣  Feature Engineering                                        │
│      ├─ ft_engineering.py                                      │
│      │   └─ FeatureEngineer.build_preprocessor()               │
│      └─ Output: train_data.csv, test_data.csv, preprocessor.pkl│
│                                                                 │
│  3️⃣  Model Training & Evaluation                                │
│      ├─ model_training_evaluation.py                           │
│      │   ├─ ModelTrainer.train_with_cross_validation()         │
│      │   ├─ 4 modelos: LR, DT, RF, GB                         │
│      │   └─ Evaluación: Accuracy, Precision, Recall, AUC      │
│      └─ Output: best_model.pkl, model_metadata.json           │
│                                                                 │
│  4️⃣  Model Deployment                                           │
│      ├─ model_deploy.py                                        │
│      │   ├─ Flask API (port 5000)                             │
│      │   ├─ Endpoints: /predict, /model-info                  │
│      │   └─ Input validation & error handling                 │
│      └─ Frontend: HTML/JS interface (port 3000)               │
│                                                                 │
│  5️⃣  Model Monitoring                                           │
│      ├─ model_monitoring.py                                    │
│      │   ├─ DriftMonitor.calculate_psi()                      │
│      │   ├─ Tests: PSI, KS test, Chi-squared                  │
│      │   └─ Alertas automáticas                               │
│      └─ streamlit_app.py                                       │
│          └─ Dashboard interactivo (port 8501)                  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 📚 Estructura del Repositorio

```
Proyecto/
├── mlops_pipeline/
│   └── src/
│       ├── cargar_datos.ipynb                  # Carga inicial de datos
│       ├── compresion_eda.ipynb                # EDA y análisis exploratorio
│       ├── ft_engineering.py                   # Feature engineering
│       ├── model_training_evaluation.py        # Entrenamiento de modelos
│       ├── model_deploy.py                     # API de deployment
│       ├── model_monitoring.py                 # Monitoreo de drift
│       └── streamlit_app.py                    # Dashboard de monitoreo
│
├── data/
│   ├── raw/
│   │   └── Churn_Modelling.csv                 # Dataset original
│   ├── processed/
│   │   ├── data_cleaned.csv                    # Datos limpios
│   │   ├── train_data.csv                      # Datos de entrenamiento
│   │   └── test_data.csv                       # Datos de test
│   └── metadata/
│       ├── eda_metadata.json                   # Metadata de EDA
│       ├── feature_engineering_metadata.json   # Metadata de FE
│       └── drift_report.json                   # Reporte de drift
│
├── models/
│   ├── best_model.pkl                          # Mejor modelo entrenado
│   ├── preprocessor.pkl                        # Pipeline de preprocesamiento
│   ├── model_metadata.json                     # Metadata del modelo
│   └── config.json                             # Configuración
│
├── frontend/
│   ├── index.html                              # Interfaz web
│   ├── server.py                               # Servidor de desarrollo
│   ├── static/
│   │   ├── css/styles.css                      # Estilos
│   │   └── js/app.js                           # Lógica del frontend
│   └── test_frontend.py                        # Tests del frontend
│
├── docker/
│   ├── Dockerfile                              # Dockerfile para API
│   ├── Dockerfile.streamlit                    # Dockerfile para dashboard
│   ├── Dockerfile.frontend                     # Dockerfile para frontend
│   ├── docker-compose.yml                      # Orquestación de servicios
│   └── docker-compose.dev.yml                  # Versión desarrollo
│
├── reports/
│   ├── deployment/
│   │   ├── DEPLOYMENT_REPORT.md                # Reporte de deployment
│   │   └── SUMMARY.md                          # Resumen ejecutivo
│   └── plots/
│       ├── confusion_matrices/                 # Matrices de confusión
│       ├── roc_curves/                         # Curvas ROC
│       ├── feature_importance/                 # Importancia de features
│       └── drift_detection/                    # Gráficos de drift
│
├── docs/
│   ├── README_PRINCIPAL.md                     # Este archivo
│   ├── README_EDA.md                           # Documentación de EDA
│   ├── README_FEATURE_ENGINEERING.md           # Documentación de FE
│   ├── README_MODEL_TRAINING.md                # Documentación de training
│   ├── README_MONITORING.md                    # Documentación de monitoring
│   ├── README_DEPLOYMENT.md                    # Documentación de deployment
│   ├── INDICE_DOCUMENTACION.md                 # Índice de navegación
│   └── docker/
│       └── DOCKER_GUIDE.md                     # Guía de Docker
│
├── scripts/
│   ├── run_pipeline.bat                        # Ejecutar pipeline completo
│   ├── start_frontend.bat                      # Iniciar frontend
│   └── QUICK_START.bat                         # Inicio rápido
│
├── requirements.txt                             # Dependencias Python
├── Makefile                                     # Comandos de automatización
├── sonar-project.properties                     # Configuración SonarQube
├── README.md                                    # README principal del repo
└── GUIA_PRUEBAS.md                             # Guía de pruebas
```

---

## 🔑 Requisitos del Checklist - Mapeo Completo

### 1️⃣ **CARGA Y EXPLORACIÓN DE DATOS (EDA)**

| Requisito | Cumplimiento | Archivo | Función/Línea | Descripción |
|-----------|--------------|---------|---------------|-------------|
| **Carga de datos CSV** | ✅ | `cargar_datos.ipynb` | Celdas 1-3 | Carga de `Churn_Modelling.csv` con pandas |
| **Análisis descriptivo** | ✅ | `compresion_eda.ipynb` | Celdas 5-8 | `df.describe()`, `df.info()` |
| **Identificación de valores nulos** | ✅ | `compresion_eda.ipynb` | Celda 9 | `df.isnull().sum()` |
| **Análisis de distribuciones** | ✅ | `compresion_eda.ipynb` | Celdas 12-18 | Histogramas, boxplots |
| **Correlaciones** | ✅ | `compresion_eda.ipynb` | Celda 20 | Matriz de correlación con seaborn |
| **Análisis de target (Churn)** | ✅ | `compresion_eda.ipynb` | Celdas 22-25 | Distribución de clases, balance |

📖 **Documentación detallada:** [docs/README_EDA.md](./README_EDA.md)

---

### 2️⃣ **PREPROCESAMIENTO Y FEATURE ENGINEERING**

| Requisito | Cumplimiento | Archivo | Función/Línea | Descripción |
|-----------|--------------|---------|---------------|-------------|
| **Pipeline de sklearn** | ✅ | `ft_engineering.py` | `build_preprocessor()` ~línea 157 | `ColumnTransformer` con pipelines |
| **Transformación numérica** | ✅ | `ft_engineering.py` | `build_preprocessor()` ~línea 170 | `StandardScaler` para features numéricas |
| **Transformación categórica** | ✅ | `ft_engineering.py` | `build_preprocessor()` ~línea 185 | `OneHotEncoder` para Geography, Gender |
| **Manejo de valores faltantes** | ✅ | `ft_engineering.py` | `build_preprocessor()` ~línea 168 | `SimpleImputer` con estrategia median/most_frequent |
| **División train/test** | ✅ | `ft_engineering.py` | `split_train_test()` ~línea 220 | `train_test_split` estratificado (80/20) |
| **Serialización de preprocessor** | ✅ | `ft_engineering.py` | `save_artifacts()` ~línea 280 | Guarda `preprocessor.pkl` con joblib |

📖 **Documentación detallada:** [docs/README_FEATURE_ENGINEERING.md](./README_FEATURE_ENGINEERING.md)

---

### 3️⃣ **ENTRENAMIENTO Y EVALUACIÓN DE MODELOS**

| Requisito | Cumplimiento | Archivo | Función/Línea | Descripción |
|-----------|--------------|---------|---------------|-------------|
| **Modelos implementados** | ✅ | `model_training_evaluation.py` | `build_models()` ~línea 122 | 4 modelos: LR, DT, RF, GB |
| **Cross-validation** | ✅ | `model_training_evaluation.py` | `train_with_cross_validation()` ~línea 159 | StratifiedKFold con 5 folds |
| **Métricas de evaluación** | ✅ | `model_training_evaluation.py` | `summarize_classification()` ~línea 256 | Accuracy, Precision, Recall, F1, AUC |
| **Matriz de confusión** | ✅ | `model_training_evaluation.py` | `plot_confusion_matrices()` ~línea 444 | Visualización para cada modelo |
| **Curva ROC** | ✅ | `model_training_evaluation.py` | `plot_roc_curves()` ~línea 393 | Comparación de AUC entre modelos |
| **Importancia de features** | ✅ | `model_training_evaluation.py` | `plot_feature_importance()` ~línea 510 | Para modelos tree-based (RF, GB) |
| **Selección del mejor modelo** | ✅ | `model_training_evaluation.py` | `select_best_model()` ~línea 340 | Basado en accuracy de validación |
| **Serialización del modelo** | ✅ | `model_training_evaluation.py` | `save_best_model()` ~línea 365 | Guarda `best_model.pkl` y metadata |

📖 **Documentación detallada:** [docs/README_MODEL_TRAINING.md](./README_MODEL_TRAINING.md)

---

### 4️⃣ **DEPLOYMENT CON API REST**

| Requisito | Cumplimiento | Archivo | Función/Línea | Descripción |
|-----------|--------------|---------|---------------|-------------|
| **Framework Flask** | ✅ | `model_deploy.py` | `app = Flask(__name__)` ~línea 30 | Aplicación Flask configurada |
| **Carga de artefactos** | ✅ | `model_deploy.py` | `load_artifacts()` ~línea 41 | Carga model.pkl y preprocessor.pkl |
| **Endpoint de predicción** | ✅ | `model_deploy.py` | `@app.route('/predict')` ~línea 145 | POST con JSON input |
| **Validación de entrada** | ✅ | `model_deploy.py` | `validate_input_data()` ~línea 82 | Valida tipos y rangos de features |
| **Manejo de errores** | ✅ | `model_deploy.py` | Try/except blocks ~líneas 165-175 | Respuestas HTTP 400/500 |
| **Endpoint de info** | ✅ | `model_deploy.py` | `@app.route('/model-info')` ~línea 203 | GET con metadata del modelo |
| **Health check** | ✅ | `model_deploy.py` | `@app.route('/')` ~línea 225 | GET para verificar estado |
| **Predicción por lotes** | ✅ | `model_deploy.py` | `/predict` acepta lista ~línea 155 | Procesa múltiples inputs |

📖 **Documentación detallada:** [docs/README_DEPLOYMENT.md](./README_DEPLOYMENT.md)

---

### 5️⃣ **MONITOREO Y DETECCIÓN DE DRIFT**

| Requisito | Cumplimiento | Archivo | Función/Línea | Descripción |
|-----------|--------------|---------|---------------|-------------|
| **Clase DriftMonitor** | ✅ | `model_monitoring.py` | `class DriftMonitor` ~línea 31 | Clase principal de monitoreo |
| **PSI (Population Stability Index)** | ✅ | `model_monitoring.py` | `calculate_psi()` ~línea 75 | Métrica para drift numérico |
| **KS Test (Kolmogorov-Smirnov)** | ✅ | `model_monitoring.py` | `detect_numerical_drift()` ~línea 159 | Test estadístico para distribuciones |
| **Chi-Squared Test** | ✅ | `model_monitoring.py` | `detect_categorical_drift()` ~línea 215 | Test para features categóricas |
| **Umbrales de alerta** | ✅ | `model_monitoring.py` | `generate_alerts()` ~línea 335 | PSI > 0.2 genera alerta |
| **Reporte de drift** | ✅ | `model_monitoring.py` | `save_drift_report()` ~línea 395 | Guarda `drift_report.json` |
| **Dashboard Streamlit** | ✅ | `streamlit_app.py` | Todo el archivo | Visualización interactiva de drift |
| **Visualización de distribuciones** | ✅ | `streamlit_app.py` | Sección "Distribuciones" ~línea 180 | Comparación baseline vs production |
| **Alertas en dashboard** | ✅ | `streamlit_app.py` | `st.warning()` ~línea 120 | Notificaciones de drift detectado |

📖 **Documentación detallada:** [docs/README_MONITORING.md](./README_MONITORING.md)

---

### 6️⃣ **CONTAINERIZACIÓN CON DOCKER**

| Requisito | Cumplimiento | Archivo | Función/Línea | Descripción |
|-----------|--------------|---------|---------------|-------------|
| **Dockerfile para API** | ✅ | `docker/Dockerfile` | Todo el archivo | Imagen Python 3.10 con Flask |
| **Dockerfile para Dashboard** | ✅ | `docker/Dockerfile.streamlit` | Todo el archivo | Imagen con Streamlit |
| **Dockerfile para Frontend** | ✅ | `docker/Dockerfile.frontend` | Todo el archivo | Imagen con servidor HTTP |
| **docker-compose.yml** | ✅ | `docker/docker-compose.yml` | Todo el archivo | Orquestación de 3 servicios |
| **Network compartida** | ✅ | `docker/docker-compose.yml` | Sección `networks` | Red mlops-network |
| **Volumes para datos** | ✅ | `docker/docker-compose.yml` | Sección `volumes` | Persistencia de models/ y data/ |
| **Health checks** | ✅ | `docker/docker-compose.yml` | Sección `healthcheck` | Verificación de servicios |
| **Multi-stage builds** | ✅ | `docker/Dockerfile` | Etapas builder/runtime | Optimización de tamaño |

📖 **Documentación detallada:** [docker/README.md](../docker/README.md)

---

## 🚀 Quick Start - Ejecutar el Proyecto

### Opción 1: Ejecución Local (Sin Docker)

```powershell
# 1. Clonar repositorio
git clone https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps.git
cd Final-ML---Dspliegue-MLOps
git checkout dev

# 2. Crear entorno virtual
python -m venv Proyecto-venv
.\Proyecto-venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar pipeline completo
python -m mlops_pipeline.src.ft_engineering
python -m mlops_pipeline.src.model_training_evaluation

# 5. Iniciar API (Terminal 1)
python -m mlops_pipeline.src.model_deploy
# API disponible en: http://localhost:5000

# 6. Iniciar Dashboard (Terminal 2)
streamlit run mlops_pipeline/src/streamlit_app.py
# Dashboard disponible en: http://localhost:8501

# 7. Iniciar Frontend (Terminal 3)
cd frontend
python server.py
# Frontend disponible en: http://localhost:3000
```

### Opción 2: Ejecución con Docker

```powershell
# 1. Construir imágenes
cd docker
docker-compose build

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Verificar servicios
docker-compose ps

# 4. Ver logs
docker-compose logs -f

# Servicios disponibles:
# - API: http://localhost:5000
# - Dashboard: http://localhost:8501
# - Frontend: http://localhost:3000

# 5. Detener servicios
docker-compose down
```

### Opción 3: Scripts de Automatización

```powershell
# Ejecutar pipeline completo
.\scripts\run_pipeline.bat

# Iniciar frontend
.\scripts\start_frontend.bat

# Quick start
.\scripts\QUICK_START.bat
```

---

## 🧪 Testing del Sistema

### Test de la API

```powershell
# Health check
curl http://localhost:5000/

# Predicción individual
$body = @{
    CreditScore = 619
    Geography = "France"
    Gender = "Female"
    Age = 42
    Tenure = 2
    Balance = 0.0
    NumOfProducts = 1
    HasCrCard = 1
    IsActiveMember = 1
    EstimatedSalary = 101348.88
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/predict" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Información del modelo
curl http://localhost:5000/model-info
```

### Test del Frontend

```powershell
# Tests automatizados
python frontend/test_frontend.py

# Test manual
# 1. Abrir http://localhost:3000
# 2. Completar formulario
# 3. Click en "Predecir"
# 4. Verificar resultado
```

### Test del Monitoreo

```powershell
# Ejecutar detección de drift
python -m mlops_pipeline.src.model_monitoring

# Verificar reporte
cat data/metadata/drift_report.json

# Ver dashboard
streamlit run mlops_pipeline/src/streamlit_app.py
```

---

## 📊 Resultados del Modelo

### Métricas de Entrenamiento

| Modelo | Accuracy | Precision | Recall | F1-Score | AUC |
|--------|----------|-----------|--------|----------|-----|
| Logistic Regression | 0.798 | 0.76 | 0.52 | 0.62 | 0.82 |
| Decision Tree | 0.789 | 0.71 | 0.55 | 0.62 | 0.78 |
| **Random Forest** | **0.865** | **0.85** | **0.73** | **0.78** | **0.89** |
| Gradient Boosting | 0.862 | 0.84 | 0.72 | 0.77 | 0.88 |

**Mejor modelo:** Random Forest con 86.5% de accuracy

### Features Más Importantes

1. **Age** (30.2%) - Edad del cliente
2. **NumOfProducts** (18.5%) - Número de productos contratados
3. **Balance** (15.8%) - Balance de la cuenta
4. **IsActiveMember** (12.3%) - Si es miembro activo
5. **CreditScore** (9.7%) - Score crediticio

---

## 🔍 Monitoreo de Drift

### Métricas de Drift

- **PSI (Population Stability Index)**
  - PSI < 0.1: Sin drift (estable)
  - 0.1 ≤ PSI < 0.2: Drift moderado (monitorear)
  - PSI ≥ 0.2: Drift significativo (reentrenar)

- **KS Test** (p-value)
  - p > 0.05: Distribuciones similares
  - p ≤ 0.05: Drift detectado

- **Chi-Squared** (features categóricas)
  - p > 0.05: Sin drift
  - p ≤ 0.05: Drift detectado

---

## 📦 Dependencias Principales

```
Python 3.10+
├── pandas >= 1.5.0         # Manipulación de datos
├── numpy >= 1.23.0          # Operaciones numéricas
├── scikit-learn >= 1.3.0    # ML algorithms y pipelines
├── matplotlib >= 3.6.0      # Visualizaciones
├── seaborn >= 0.12.0        # Visualizaciones estadísticas
├── flask >= 3.0.0           # API REST
├── flask-cors >= 4.0.0      # CORS para API
├── streamlit >= 1.28.0      # Dashboard interactivo
├── scipy >= 1.10.0          # Tests estadísticos
└── joblib >= 1.3.0          # Serialización de modelos
```

---

## 🗂️ Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA FLOW                             │
└─────────────────────────────────────────────────────────────┘

  data/raw/Churn_Modelling.csv
           │
           │ (1) EDA & Cleaning
           ├─> compresion_eda.ipynb
           │   └─> data/processed/data_cleaned.csv
           │
           │ (2) Feature Engineering
           ├─> ft_engineering.py
           │   ├─> data/processed/train_data.csv
           │   ├─> data/processed/test_data.csv
           │   └─> models/preprocessor.pkl
           │
           │ (3) Model Training
           ├─> model_training_evaluation.py
           │   ├─> models/best_model.pkl
           │   ├─> models/model_metadata.json
           │   └─> reports/plots/*.png
           │
           │ (4) Model Deployment
           ├─> model_deploy.py
           │   └─> API REST (Flask) :5000
           │       ├─> POST /predict
           │       └─> GET /model-info
           │
           │ (5) Model Monitoring
           └─> model_monitoring.py
               ├─> data/metadata/drift_report.json
               └─> streamlit_app.py
                   └─> Dashboard :8501
```

---

## 🛠️ Comandos Útiles

### Gestión del Entorno

```powershell
# Activar entorno virtual
.\Proyecto-venv\Scripts\Activate.ps1

# Desactivar entorno
deactivate

# Instalar dependencias
pip install -r requirements.txt

# Actualizar dependencias
pip freeze > requirements.txt
```

### Ejecución de Módulos

```powershell
# Feature Engineering
python -m mlops_pipeline.src.ft_engineering

# Entrenamiento
python -m mlops_pipeline.src.model_training_evaluation

# API
python -m mlops_pipeline.src.model_deploy

# Monitoreo
python -m mlops_pipeline.src.model_monitoring

# Dashboard
streamlit run mlops_pipeline/src/streamlit_app.py
```

### Docker

```powershell
# Build
docker-compose -f docker/docker-compose.yml build

# Start
docker-compose -f docker/docker-compose.yml up -d

# Stop
docker-compose -f docker/docker-compose.yml down

# Logs
docker-compose -f docker/docker-compose.yml logs -f

# Restart servicio específico
docker-compose restart mlops-api
```

---

## 📖 Documentación Completa

### Documentación por Módulo

1. **[EDA](./README_EDA.md)** - Análisis exploratorio de datos
2. **[Feature Engineering](./README_FEATURE_ENGINEERING.md)** - Preprocesamiento y pipelines
3. **[Model Training](./README_MODEL_TRAINING.md)** - Entrenamiento y evaluación
4. **[Deployment](./README_DEPLOYMENT.md)** - API REST con Flask
5. **[Monitoring](./README_MONITORING.md)** - Detección de drift

### Documentación de Infraestructura

- **[Docker Guide](./docker/DOCKER_GUIDE.md)** - Guía completa de Docker
- **[Data README](../data/README.md)** - Estructura de datos
- **[Models README](../models/README.md)** - Artefactos del modelo
- **[Frontend README](../frontend/README.md)** - Interfaz web
- **[Reports README](../reports/README.md)** - Reportes y visualizaciones

### Índice de Navegación

📑 **[INDICE_DOCUMENTACION.md](./INDICE_DOCUMENTACION.md)** - Navegación completa por toda la documentación

---

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📝 Licencia

Este proyecto es parte de un trabajo académico para el curso de Machine Learning.

---

## 👥 Equipo

- **Repositorio:** MiguelRodriguez09/Final-ML---Dspliegue-MLOps
- **Branch principal:** dev
- **Documentación:** docs/

---

## 🔗 Enlaces Útiles

- [Repositorio GitHub](https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps)
- [Documentación Scikit-learn](https://scikit-learn.org/)
- [Documentación Flask](https://flask.palletsprojects.com/)
- [Documentación Streamlit](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📞 Soporte

Para preguntas o problemas:
- Revisar la [documentación completa](./INDICE_DOCUMENTACION.md)
- Abrir un issue en GitHub
- Consultar los READMEs específicos de cada módulo

---

**Última actualización:** 2024
**Versión:** 1.0.0
