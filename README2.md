# 🧠 Proyecto MLOps - Predicción de Churn Bancario

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este repositorio implementa un **pipeline completo de MLOps** para la predicción de churn (abandono) de clientes bancarios, siguiendo las mejores prácticas de calidad de código y arquitectura de software.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Caso de Negocio](#-caso-de-negocio)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Principales Hallazgos del EDA](#-principales-hallazgos-del-eda)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso del Pipeline](#-uso-del-pipeline)
- [API de Predicción](#-api-de-predicción)
- [Monitoreo y Drift Detection](#-monitoreo-y-drift-detection)
- [Despliegue con Docker](#-despliegue-con-docker)
- [Calidad de Código](#-calidad-de-código)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa un **pipeline end-to-end de Machine Learning** con enfoque en MLOps, que incluye:

- ✅ **Análisis Exploratorio de Datos (EDA)** con funciones genéricas y reutilizables
- ✅ **Feature Engineering** automatizado usando sklearn pipelines
- ✅ **Entrenamiento y evaluación** de múltiples modelos de clasificación
- ✅ **Despliegue** mediante API REST (Flask)
- ✅ **Monitoreo de Data Drift** con métricas estadísticas (PSI, KS, Chi²)
- ✅ **Dashboard de visualización** con Streamlit
- ✅ **Contenerización** con Docker
- ✅ **Código limpio** validado con SonarCloud

---

## 💼 Caso de Negocio

### Problema

Una institución bancaria enfrenta un alto índice de **abandono de clientes (churn)**, lo que resulta en pérdidas significativas de ingresos y costos elevados de adquisición de nuevos clientes.

### Solución

Implementar un **modelo predictivo** que identifique clientes con alto riesgo de abandono, permitiendo:

- 🎯 **Retención proactiva**: Intervenciones tempranas con clientes en riesgo
- 💰 **Optimización de recursos**: Focalizar esfuerzos en clientes con mayor probabilidad de churn
- 📊 **Monitoreo continuo**: Detectar cambios en los patrones de comportamiento

### Impacto Esperado

- Reducción del 15-25% en la tasa de churn
- Aumento del ROI en campañas de retención
- Mejor comprensión de los factores que influyen en la decisión de abandono

---

## 🏗️ Arquitectura del Proyecto

```
┌─────────────────┐
│  Datos Crudos   │
│ (Churn CSV)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ EDA & Limpieza  │
│  (Notebooks)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Feature      │
│  Engineering    │
│  (Pipelines)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Entrenamiento  │
│   4 Modelos     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Evaluación    │
│  & Selección    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Modelo          │
│ Seleccionado    │
└────┬───────┬────┘
     │       │
     │       ▼
     │  ┌─────────────────┐
     │  │   Monitoreo     │
     │  │   Data Drift    │
     │  └────────┬────────┘
     │           │
     │           ▼
     │      ┌─────────┐
     │      │¿Drift?  │
     │      └────┬────┘
     │           │
     │      ┌────┴────┐
     │      │         │
     │      ▼         ▼
     │   [SÍ]      [NO]
     │      │         │
     │      ▼         │
     │  ┌──────┐     │
     │  │Alerta│     │
     │  └──────┘     │
     │               │
     ▼               ▼
┌─────────────────────┐
│  API Predicción     │
│    (Flask)          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Dashboard         │
│   (Streamlit)       │
└─────────────────────┘
```

---

## 📊 Principales Hallazgos del EDA

### Dataset: Churn Modelling

- **Registros**: 10,000 clientes
- **Variables**: 14 características (11 features + 3 identificadores)
- **Target**: `Exited` (1 = Churn, 0 = Retención)

### Hallazgos Clave

#### 1. **Desbalance de Clases**
   - Churn (1): ~20.4%
   - Retención (0): ~79.6%
   - **Acción**: Considerar técnicas de balanceo (SMOTE, class_weight)

#### 2. **Variables Más Relevantes**
   - **Age (Edad)**: Clientes mayores tienen mayor tasa de churn
   - **Geography (Geografía)**: Alemania tiene mayor churn que Francia/España
   - **NumOfProducts**: Clientes con 3-4 productos tienen mayor riesgo
   - **IsActiveMember**: Miembros inactivos tienen 2x más probabilidad de churn
   - **Balance**: Correlación moderada con churn

#### 3. **Patrones Identificados**
   - Edad promedio de churn: 44 años vs. 37 años (no churn)
   - 50% del churn proviene de clientes con balance > $100k
   - Clientes con CreditScore bajo (<400) tienen mayor riesgo

#### 4. **Calidad de Datos**
   - ✅ Sin valores nulos
   - ✅ Sin duplicados
   - ⚠️ Variables irrelevantes identificadas: RowNumber, CustomerId, Surname

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.10 o superior
- pip
- Git
- (Opcional) Docker

### Instalación

#### 1. **Clonar el repositorio**:

```bash
git clone https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps.git
cd Proyecto
```

#### 2. **Crear entorno virtual** (Recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

O usar el script automatizado:

```bash
# Windows
set_up.bat
```

---

## 📦 Uso del Pipeline

### 1. Carga de Datos

```bash
jupyter notebook mlops_pipeline/src/cargar_datos.ipynb
```

**Descripción**: Carga el dataset `Churn_Modelling.csv` y realiza una inspección inicial.

### 2. Análisis Exploratorio (EDA)

```bash
jupyter notebook mlops_pipeline/src/compresion_eda.ipynb
```

**Funcionalidades**:
- Clasificación automática de variables
- Análisis univariable y bivariable completo
- Generación de reglas de validación
- Recomendaciones para feature engineering

**Salidas**:
- `data_cleaned.csv`: Dataset limpio
- `eda_metadata.json`: Metadatos y reglas de validación

### 3. Feature Engineering

```bash
python mlops_pipeline/src/ft_engineering.py
```

**Características**:
- Usa sklearn Pipelines con ColumnTransformer
- Transformaciones específicas por tipo de variable
- Separación estratificada train/test (80/20)

**Salidas**:
- `train_data.csv` y `test_data.csv`: Datos procesados
- `preprocessor.pkl`: Pipeline de transformación serializado
- `feature_engineering_metadata.json`: Metadatos

### 4. Entrenamiento y Evaluación

```bash
python mlops_pipeline/src/model_training_evaluation.py
```

**Modelos Evaluados**:
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

**Métricas Calculadas**:
- Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Validación cruzada (5-fold stratified)
- Análisis de overfitting

**Salidas**:
- `best_model.pkl`: Mejor modelo seleccionado
- `model_metadata.json`: Métricas del modelo
- Visualizaciones:
  - `model_comparison.png`: Comparación de todos los modelos
  - `confusion_matrices.png`: Matrices de confusión
  - `roc_curves.png`: Curvas ROC

---

## 🌐 API de Predicción

### Iniciar el Servidor

```bash
python mlops_pipeline/src/model_deploy.py
```

El servidor estará disponible en: `http://localhost:5000`

### Endpoints

#### 1. **Health Check**

```bash
GET /
```

**Respuesta**:
```json
{
  "status": "healthy",
  "service": "MLOps Model API",
  "model_loaded": true,
  "preprocessor_loaded": true
}
```

#### 2. **Información del Modelo**

```bash
GET /model-info
```

**Respuesta**:
```json
{
  "model_name": "Random Forest",
  "model_type": "RandomForestClassifier",
  "metrics": {
    "test_accuracy": 0.8640,
    "test_f1": 0.5847,
    "test_roc_auc": 0.8524
  },
  "n_features": 15
}
```

#### 3. **Predicción Individual (JSON)**

```bash
POST /predict
Content-Type: application/json

{
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
}
```

**Respuesta**:
```json
{
  "success": true,
  "predictions": [1],
  "probabilities": [[0.32, 0.68]],
  "n_samples": 1,
  "model": "Random Forest"
}
```

#### 4. **Predicción por Lotes (JSON Array)**

```bash
POST /predict-batch
Content-Type: application/json

[
  {
    "CreditScore": 619,
    "Age": 42,
    "Geography": "France",
    ...
  },
  {
    "CreditScore": 608,
    "Age": 41,
    "Geography": "Spain",
    ...
  }
]
```

**Respuesta**:
```json
{
  "success": true,
  "n_samples": 2,
  "predictions": [
    {
      "index": 0,
      "prediction": 1,
      "probability": [0.32, 0.68]
    },
    {
      "index": 1,
      "prediction": 0,
      "probability": [0.85, 0.15]
    }
  ],
  "model": "Random Forest"
}
```

#### 5. **Predicción con CSV**

```bash
POST /predict
Content-Type: multipart/form-data
file: customers.csv
```

### Ejemplo con Python

```python
import requests

# URL del servidor
url = "http://localhost:5000/predict"

# Datos del cliente
data = {
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
}

# Realizar predicción
response = requests.post(url, json=data)
result = response.json()

print(f"Predicción: {result['predictions'][0]}")
print(f"Probabilidad de churn: {result['probabilities'][0][1]:.2%}")
```

### Ejemplo con cURL

```bash
# Windows PowerShell
$body = @{
    CreditScore = 619
    Geography = "France"
    Gender = "Female"
    Age = 42
    Tenure = 2
    Balance = 0
    NumOfProducts = 1
    HasCrCard = 1
    IsActiveMember = 1
    EstimatedSalary = 101348.88
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post -Body $body -ContentType "application/json"
```

---

## 📈 Monitoreo y Drift Detection

### Ejecutar Análisis de Drift

```bash
python mlops_pipeline/src/model_monitoring.py
```

### Métricas de Drift Implementadas

#### **PSI (Population Stability Index)** - Variables Numéricas
Mide el cambio en la distribución de una variable entre dos períodos.

**Interpretación**:
- PSI < 0.1: **Drift bajo** ✅ - Sin cambios significativos
- 0.1 ≤ PSI < 0.2: **Drift moderado** ⚠️ - Monitoreo cercano
- PSI ≥ 0.2: **Drift alto** 🚨 - Requiere acción inmediata

#### **Test de Kolmogorov-Smirnov** - Variables Numéricas
Compara dos distribuciones para detectar diferencias significativas.

**Interpretación**:
- p-value > 0.05: Distribuciones similares ✅
- p-value ≤ 0.05: Distribuciones diferentes 🚨

#### **Test Chi-cuadrado** - Variables Categóricas
Evalúa la independencia entre distribuciones categóricas.

**Interpretación**:
- p-value > 0.05: No hay asociación significativa ✅
- p-value ≤ 0.05: Asociación significativa detectada 🚨

### Sistema de Alertas

El sistema genera alertas automáticas cuando:
1. **Drift Alto** (PSI ≥ 0.2): Alerta crítica con recomendación de reentrenamiento
2. **Drift Moderado** (0.1 ≤ PSI < 0.2): Advertencia de monitoreo cercano
3. **Múltiples Variables** (>30%): Recomendación urgente de reentrenamiento

### Dashboard de Monitoreo (Streamlit)

```bash
streamlit run mlops_pipeline/src/streamlit_app.py
```

El dashboard estará disponible en: `http://localhost:8501`

#### **Funcionalidades del Dashboard**:

1. **📊 Métricas de Resumen**:
   - Columnas analizadas
   - Drift detectado (cantidad y porcentaje)
   - Estado del sistema (semáforo: 🟢 🟡 🔴)

2. **📈 Tab "Resumen"**:
   - Gráfico de pastel: Distribución de drift
   - Gráfico de barras: Severidad del drift (bajo/moderado/alto)

3. **📊 Tab "Métricas PSI"**:
   - Gráfico horizontal de PSI por variable
   - Línea de umbral (0.2)
   - Tabla detallada con valores

4. **🚨 Tab "Alertas"**:
   - Alertas por variable con código de colores
   - Métricas específicas (PSI, Chi², p-values)
   - Recomendaciones automáticas

5. **🔍 Tab "Análisis Detallado"**:
   - Selector de variables
   - Comparación de estadísticas descriptivas
   - Distribuciones de referencia vs. actuales

---

## 🐳 Despliegue con Docker

### Construir la Imagen

```bash
docker build -t mlops-api:latest .
```

**Tiempo estimado**: 2-3 minutos (primera vez)

### Ejecutar el Contenedor

```bash
docker run -d -p 5000:5000 --name mlops-api mlops-api:latest
```

**Opciones**:
- `-d`: Ejecutar en modo detached (background)
- `-p 5000:5000`: Mapear puerto 5000 del contenedor al host
- `--name mlops-api`: Nombre del contenedor

### Verificar el Servicio

```bash
# Health check
curl http://localhost:5000/

# Logs del contenedor
docker logs mlops-api

# Verificar contenedor en ejecución
docker ps
```

### Detener y Eliminar

```bash
# Detener el contenedor
docker stop mlops-api

# Eliminar el contenedor
docker rm mlops-api

# Eliminar la imagen (opcional)
docker rmi mlops-api:latest
```

### Docker Compose (Opcional)

Crear `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mlops-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

Ejecutar:

```bash
docker-compose up -d
docker-compose down
```

---

## ✅ Calidad de Código

### SonarCloud

El proyecto está configurado para ser analizado con **SonarCloud**, asegurando:

- ✅ **Mantenibilidad**: Código limpio y fácil de mantener
- ✅ **Confiabilidad**: Sin bugs críticos
- ✅ **Seguridad**: Sin vulnerabilidades
- ✅ **Cobertura**: Tests adecuados (cuando se implementen)

**Archivo de configuración**: `sonar-project.properties`

### Mejores Prácticas Implementadas

#### 1. **Documentación Completa**
```python
def calculate_psi(reference: np.ndarray, current: np.ndarray, n_bins: int = 10) -> float:
    """
    Calcula el Population Stability Index (PSI).
    
    Args:
        reference: Datos de referencia
        current: Datos actuales
        n_bins: Número de bins para discretización
    
    Returns:
        Valor de PSI
    """
```

#### 2. **Type Hints**
```python
def load_data(self) -> pd.DataFrame:
def split_features_target(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
```

#### 3. **Logging Estructurado**
```python
logger.info(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
logger.warning(f"Columna {col} no encontrada en datos actuales")
logger.error(f"Error al cargar artefactos: {e}")
```

#### 4. **Error Handling Robusto**
```python
try:
    model = joblib.load(model_path)
except FileNotFoundError as e:
    logger.error(f"Error al cargar artefactos: {e}")
    raise
except Exception as e:
    logger.error(f"Error inesperado: {e}")
    raise
```

#### 5. **Código DRY (Don't Repeat Yourself)**
- Funciones reutilizables y genéricas
- Clases con métodos modulares
- Herencia y composición cuando es apropiado

#### 6. **Separación de Responsabilidades**
- Cada clase tiene un propósito único
- Módulos organizados por funcionalidad
- API, lógica de negocio y persistencia separadas

### Pipeline CI/CD

**Archivo**: `.github/workflows/ci-cd.yml`

**Jobs**:
1. **quality-check**: Linting con flake8 + SonarCloud scan
2. **test**: Ejecución de tests unitarios (cuando se implementen)
3. **build-docker**: Construcción y testing de imagen Docker

---

## 📁 Estructura del Proyecto

```
Proyecto/
│
├── mlops_pipeline/              # Pipeline principal de MLOps
│   └── src/
│       ├── cargar_datos.ipynb           # 📓 Carga inicial de datos
│       ├── compresion_eda.ipynb         # 📊 EDA completo con funciones genéricas
│       ├── ft_engineering.py            # 🔧 Feature engineering con pipelines
│       ├── model_training_evaluation.py # 🤖 Entrenamiento y evaluación
│       ├── model_deploy.py              # 🌐 API REST con Flask
│       ├── model_monitoring.py          # 📈 Detección de drift
│       └── streamlit_app.py             # 📊 Dashboard de monitoreo
│
├── Directrices/                 # Documentación del proyecto
│   └── directriz_definitiva.md          # Guía completa del proyecto
│
├── .github/                     # Configuración de GitHub
│   └── workflows/
│       └── ci-cd.yml                    # Pipeline CI/CD
│
├── Churn_Modelling.csv          # 📄 Dataset original (10,000 registros)
├── config.json                  # ⚙️ Configuración del proyecto
├── requirements.txt             # 📦 Dependencias Python
├── Dockerfile                   # 🐳 Configuración Docker
├── .dockerignore                # 🐳 Exclusiones Docker
├── .gitignore                   # 📋 Exclusiones Git
├── sonar-project.properties     # 🔍 Configuración SonarCloud
│
├── set_up.bat                   # 🔧 Script de setup (Windows)
├── run_pipeline.bat             # ▶️ Script de ejecución automatizada
│
├── readme.md                    # 📖 README original
├── README2.md                   # 📖 README completo (este archivo)
├── QUICKSTART.md                # 🚀 Guía de inicio rápido
└── SUMMARY.md                   # 📝 Resumen de implementación

# Archivos generados durante la ejecución:
├── data_cleaned.csv                    # Dataset limpio (EDA)
├── eda_metadata.json                   # Metadatos del EDA
├── train_data.csv                      # Datos de entrenamiento procesados
├── test_data.csv                       # Datos de prueba procesados
├── preprocessor.pkl                    # Pipeline de transformación
├── feature_engineering_metadata.json   # Metadatos de FE
├── best_model.pkl                      # Mejor modelo entrenado
├── model_metadata.json                 # Métricas del modelo
├── model_comparison.png                # Gráfico: Comparación de modelos
├── confusion_matrices.png              # Gráfico: Matrices de confusión
├── roc_curves.png                      # Gráfico: Curvas ROC
├── drift_report.json                   # Reporte de drift
└── drift_summary.png                   # Gráfico: Resumen de drift
```

---

## 🛠️ Tecnologías Utilizadas

### Core ML & Data Science
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.10+ | Lenguaje principal |
| **pandas** | 2.0+ | Manipulación de datos |
| **numpy** | 1.24+ | Operaciones numéricas |
| **scikit-learn** | 1.3+ | Machine Learning (pipelines, modelos, métricas) |
| **xgboost** | 2.0+ | Gradient Boosting avanzado |
| **lightgbm** | 4.0+ | Gradient Boosting eficiente |
| **scipy** | 1.10+ | Estadística y tests (KS, Chi²) |

### Visualización
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **matplotlib** | 3.7+ | Gráficos estáticos |
| **seaborn** | 0.12+ | Visualizaciones estadísticas |
| **plotly** | 5.17+ | Gráficos interactivos (dashboard) |

### Deployment & API
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Flask** | 3.0+ | Framework web para API REST |
| **flask-cors** | 4.0+ | CORS para API |
| **joblib** | 1.3+ | Serialización de modelos |

### Monitoreo & Dashboard
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **streamlit** | 1.28+ | Dashboard web interactivo |
| **evidently** | 0.4+ | Detección de drift (opcional) |

### DevOps
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Docker** | Latest | Contenerización |
| **Git** | Latest | Control de versiones |
| **GitHub Actions** | - | CI/CD |
| **SonarCloud** | - | Análisis de calidad de código |

### Jupyter
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **jupyter** | 1.0+ | Notebooks interactivos |
| **ipykernel** | 6.25+ | Kernel de Python para notebooks |
| **notebook** | 7.0+ | Interfaz de notebooks |

### Utilities
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **python-dateutil** | 2.8+ | Manejo de fechas |
| **pytz** | 2023.3+ | Zonas horarias |
| **tqdm** | 4.65+ | Barras de progreso |

---

## 📞 Contacto y Soporte

Si tienes preguntas o necesitas soporte:

1. 🐛 **Reportar un bug**: 
   - Abre un [issue](https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps/issues)
   - Incluye descripción detallada y pasos para reproducir

2. 💡 **Sugerir mejoras**: 
   - Abre un [pull request](https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps/pulls)
   - Describe claramente los cambios propuestos

3. 📧 **Contacto directo**: 
   - [Crea un issue](https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps/issues/new)

4. 📖 **Documentación adicional**:
   - Ver `QUICKSTART.md` para inicio rápido
   - Ver `SUMMARY.md` para resumen de implementación

---

## 📚 Referencias y Recursos

### Dataset
- **Fuente**: [Kaggle - Bank Customer Churn Prediction](https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction)
- **Licencia**: Open Database License

### Inspiración y Mejores Prácticas
- [MLOps Principles](https://ml-ops.org/)
- [Google - Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Scikit-learn Best Practices](https://scikit-learn.org/stable/developers/develop.html)
- [Flask API Best Practices](https://flask.palletsprojects.com/en/3.0.x/api/)

### Herramientas de Calidad
- [PEP 8 Style Guide](https://pep8.org/)
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 🔄 Changelog

### Version 1.0.0 (Noviembre 2025)
- ✅ Implementación completa del pipeline MLOps
- ✅ EDA con funciones genéricas y reutilizables
- ✅ Feature Engineering con sklearn pipelines
- ✅ Entrenamiento de 4 modelos de clasificación
- ✅ API REST con Flask (4 endpoints)
- ✅ Sistema de monitoreo de drift (PSI, KS, Chi²)
- ✅ Dashboard interactivo con Streamlit
- ✅ Contenerización con Docker
- ✅ CI/CD con GitHub Actions
- ✅ Configuración de SonarCloud
- ✅ Documentación completa

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2025 Miguel Rodriguez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Agradecimientos

- **Kaggle** por proporcionar el dataset
- **Comunidad de MLOps** por las mejores prácticas
- **scikit-learn** por el excelente framework de ML
- **Flask** y **Streamlit** por facilitar el despliegue
- **Docker** por simplificar la contenerización

---

## 🎓 Aprendizajes Clave

Este proyecto demuestra:

1. **Implementación End-to-End**: Desde EDA hasta despliegue
2. **Código de Producción**: Limpio, documentado y mantenible
3. **Arquitectura MLOps**: Monitoreo, drift detection, CI/CD
4. **Reutilizabilidad**: Funciones genéricas aplicables a otros datasets
5. **Best Practices**: Type hints, logging, error handling, testing

---

<p align="center">
  <strong>⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/MiguelRodriguez09/Final-ML---Dspliegue-MLOps?style=social" alt="GitHub stars">
  <img src="https://img.shields.io/github/forks/MiguelRodriguez09/Final-ML---Dspliegue-MLOps?style=social" alt="GitHub forks">
</p>

<p align="center">
  Hecho con ❤️ y ☕
</p>

<p align="center">
  <sub>Proyecto MLOps - Predicción de Churn Bancario | 2025</sub>
</p>
