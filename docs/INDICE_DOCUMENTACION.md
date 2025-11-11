# 📑 ÍNDICE DE DOCUMENTACIÓN - MLOps Project

## 🏠 Inicio Rápido

¿No sabes por dónde empezar? Sigue esta guía:

1. **🎯 [README Principal](./README_PRINCIPAL.md)** - Empieza aquí para entender el proyecto completo
2. **🚀 Quick Start** - Sigue las instrucciones de ejecución en el README Principal
3. **📚 Módulos** - Explora la documentación específica según lo que necesites

---

## 📚 Documentación por Módulo

### 🔍 1. EDA (Exploratory Data Analysis)

**Archivo:** [docs/README_EDA.md](./README_EDA.md)

**Contenido:**
- 📊 Análisis descriptivo de datos
- 🔍 Identificación de valores nulos
- 📈 Visualización de distribuciones
- 🔗 Matriz de correlaciones
- ⚖️ Análisis de balance de clases

**Notebooks:**
- `mlops_pipeline/src/cargar_datos.ipynb`
- `mlops_pipeline/src/compresion_eda.ipynb`

**Outputs:**
- `data/processed/data_cleaned.csv`
- `data/metadata/eda_metadata.json`

**¿Cuándo usar?**
- ✅ Necesitas entender la estructura de los datos
- ✅ Quieres ver cómo se realizó el análisis exploratorio
- ✅ Buscas información sobre las distribuciones de features

---

### 🔧 2. Feature Engineering

**Archivo:** [docs/README_FEATURE_ENGINEERING.md](./README_FEATURE_ENGINEERING.md)

**Contenido:**
- 🔀 Pipelines de sklearn
- 📏 Escalado de features numéricas (StandardScaler)
- 🏷️ Encoding de features categóricas (OneHotEncoder)
- 🔄 ColumnTransformer
- ✂️ División train/test estratificada

**Script principal:**
- `mlops_pipeline/src/ft_engineering.py`

**Funciones clave:**
- `FeatureEngineer.build_preprocessor()` - Línea ~157
- `FeatureEngineer.split_train_test()` - Línea ~220
- `FeatureEngineer.save_artifacts()` - Línea ~280

**Outputs:**
- `data/processed/train_data.csv` (8000 filas, 80%)
- `data/processed/test_data.csv` (2000 filas, 20%)
- `models/preprocessor.pkl` (~50 KB)
- `data/metadata/feature_engineering_metadata.json`

**¿Cuándo usar?**
- ✅ Necesitas modificar el pipeline de preprocesamiento
- ✅ Quieres agregar nuevas transformaciones
- ✅ Buscas entender cómo se procesan los datos antes del modelo

---

### 🤖 3. Model Training & Evaluation

**Archivo:** [docs/README_MODEL_TRAINING.md](./README_MODEL_TRAINING.md)

**Contenido:**
- 🎯 4 modelos implementados (LR, DT, RF, GB)
- 📊 Cross-validation con StratifiedKFold (5 folds)
- 📈 Métricas: Accuracy, Precision, Recall, F1-Score, AUC
- 🎨 Visualizaciones: Confusion Matrix, ROC Curve, Feature Importance
- 🏆 Selección del mejor modelo

**Script principal:**
- `mlops_pipeline/src/model_training_evaluation.py`

**Funciones clave:**
- `ModelTrainer.build_models()` - Línea ~122
- `ModelTrainer.train_with_cross_validation()` - Línea ~159
- `ModelTrainer.summarize_classification()` - Línea ~256
- `ModelTrainer.select_best_model()` - Línea ~340
- `ModelTrainer.plot_roc_curves()` - Línea ~393
- `ModelTrainer.plot_confusion_matrices()` - Línea ~444
- `ModelTrainer.plot_feature_importance()` - Línea ~510

**Outputs:**
- `models/best_model.pkl` (15-30 MB)
- `models/model_metadata.json`
- `reports/plots/confusion_matrices/*.png`
- `reports/plots/roc_curves/*.png`
- `reports/plots/feature_importance/*.png`

**¿Cuándo usar?**
- ✅ Quieres agregar un nuevo modelo
- ✅ Necesitas modificar hiperparámetros
- ✅ Buscas mejorar las métricas de evaluación
- ✅ Quieres entender cómo se selecciona el mejor modelo

---

### 🚀 4. Model Deployment (API REST)

**Archivo:** [docs/README_DEPLOYMENT.md](./README_DEPLOYMENT.md)

**Contenido:**
- 🌐 API REST con Flask
- 🔌 3 endpoints principales
  - `POST /predict` - Predicción individual o por lotes
  - `GET /model-info` - Información del modelo
  - `GET /` - Health check
- ✅ Validación de entrada
- ⚠️ Manejo de errores
- 📦 CORS habilitado

**Script principal:**
- `mlops_pipeline/src/model_deploy.py`

**Funciones clave:**
- `load_artifacts()` - Línea ~41
- `validate_input_data()` - Línea ~82
- `predict()` - Línea ~145 (endpoint principal)
- `model_info()` - Línea ~203
- `health_check()` - Línea ~225

**Inputs esperados:**
```json
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

**¿Cuándo usar?**
- ✅ Necesitas hacer predicciones en producción
- ✅ Quieres integrar el modelo con otras aplicaciones
- ✅ Buscas agregar nuevos endpoints a la API
- ✅ Necesitas modificar la validación de entrada

---

### 📊 5. Model Monitoring & Drift Detection

**Archivo:** [docs/README_MONITORING.md](./README_MONITORING.md)

**Contenido:**
- 🔍 Detección de drift de datos
- 📉 PSI (Population Stability Index)
- 📊 KS Test (Kolmogorov-Smirnov)
- 🔬 Chi-Squared Test
- 🚨 Sistema de alertas automático
- 📱 Dashboard interactivo con Streamlit

**Scripts principales:**
- `mlops_pipeline/src/model_monitoring.py`
- `mlops_pipeline/src/streamlit_app.py`

**Funciones clave (model_monitoring.py):**
- `DriftMonitor.__init__()` - Línea ~31
- `DriftMonitor.calculate_psi()` - Línea ~75
- `DriftMonitor.detect_numerical_drift()` - Línea ~159
- `DriftMonitor.detect_categorical_drift()` - Línea ~215
- `DriftMonitor.run_drift_detection()` - Línea ~280
- `DriftMonitor.generate_alerts()` - Línea ~335
- `DriftMonitor.save_drift_report()` - Línea ~395

**Dashboard (streamlit_app.py):**
- Visualización de métricas de drift
- Comparación de distribuciones
- Alertas en tiempo real
- Exportación de reportes

**Outputs:**
- `data/metadata/drift_report.json`
- `reports/plots/drift_detection/*.png`

**Umbrales de alerta:**
- PSI < 0.1: ✅ Sin drift (verde)
- 0.1 ≤ PSI < 0.2: ⚠️ Drift moderado (amarillo)
- PSI ≥ 0.2: 🚨 Drift crítico (rojo)

**¿Cuándo usar?**
- ✅ Necesitas monitorear el modelo en producción
- ✅ Quieres detectar cambios en los datos
- ✅ Buscas saber cuándo reentrenar el modelo
- ✅ Quieres visualizar las distribuciones de datos

---

## 🏗️ Documentación de Infraestructura

### 🐳 Docker & Containerization

**Archivo:** [docker/README.md](../docker/README.md)

**Contenido:**
- 📦 Dockerfiles para 3 servicios
  - API (Flask) - Puerto 5000
  - Dashboard (Streamlit) - Puerto 8501
  - Frontend (HTTP Server) - Puerto 3000
- 🔗 Docker Compose para orquestación
- 🌐 Networking entre contenedores
- 💾 Volumes para persistencia
- ❤️ Health checks
- ☁️ Deployment en cloud (AWS, Azure, GCP)

**Archivos:**
- `docker/Dockerfile` - API
- `docker/Dockerfile.streamlit` - Dashboard
- `docker/Dockerfile.frontend` - Frontend
- `docker/docker-compose.yml` - Producción
- `docker/docker-compose.dev.yml` - Desarrollo

**Comandos principales:**
```powershell
# Build
docker-compose -f docker/docker-compose.yml build

# Start
docker-compose -f docker/docker-compose.yml up -d

# Stop
docker-compose -f docker/docker-compose.yml down

# Logs
docker-compose -f docker/docker-compose.yml logs -f
```

**¿Cuándo usar?**
- ✅ Quieres deployar el sistema completo
- ✅ Necesitas reproducibilidad del entorno
- ✅ Buscas deployar en cloud
- ✅ Quieres escalar los servicios

---

### 💾 Data Structure

**Archivo:** [data/README.md](../data/README.md)

**Contenido:**
- 📁 Estructura de carpetas de datos
  - `raw/` - Datos originales sin procesar
  - `processed/` - Datos limpios y splits
  - `metadata/` - Archivos de metadata y reportes
- 📄 Descripción de cada archivo
- 🔄 Flujo de datos
- 📋 Versionado de datos
- 🔁 Estrategias de reproducibilidad

**Archivos principales:**
- `raw/Churn_Modelling.csv` - Dataset original (10,000 filas)
- `processed/data_cleaned.csv` - Datos después de EDA
- `processed/train_data.csv` - Set de entrenamiento (8,000 filas)
- `processed/test_data.csv` - Set de prueba (2,000 filas)
- `metadata/eda_metadata.json` - Metadata de EDA
- `metadata/feature_engineering_metadata.json` - Metadata de FE
- `metadata/drift_report.json` - Reporte de drift

**¿Cuándo usar?**
- ✅ Necesitas entender la estructura de datos
- ✅ Quieres agregar nuevos datasets
- ✅ Buscas versionar los datos
- ✅ Necesitas reproducir el flujo de datos

---

### 🎯 Models Artifacts

**Archivo:** [models/README.md](../models/README.md)

**Contenido:**
- 🧠 Artefactos del modelo
  - `best_model.pkl` - Modelo entrenado (15-30 MB)
  - `preprocessor.pkl` - Pipeline de preprocesamiento (~50 KB)
  - `model_metadata.json` - Metadata del modelo
  - `config.json` - Configuración
- 📦 Versionado de modelos
- 🔄 Estrategias de carga/guardado
- 🔐 Compatibilidad y seguridad

**Información en metadata:**
```json
{
  "model_name": "Random Forest",
  "model_version": "v1.0.0",
  "training_date": "2024-01-15",
  "metrics": {
    "accuracy": 0.865,
    "precision": 0.85,
    "recall": 0.73,
    "f1_score": 0.78,
    "roc_auc": 0.89
  },
  "features": [...],
  "sklearn_version": "1.3.0"
}
```

**¿Cuándo usar?**
- ✅ Necesitas cargar el modelo en producción
- ✅ Quieres versionar modelos
- ✅ Buscas información sobre el modelo actual
- ✅ Necesitas verificar compatibilidad

---

### 🎨 Frontend & UI

**Archivo:** [frontend/README.md](../frontend/README.md)

**Contenido:**
- 🌐 Interfaz web de usuario
- 📝 Formulario de predicción
- 📊 Visualización de resultados
- 🎨 Diseño responsivo
- ✅ Validación de entrada
- 🧪 Tests automatizados

**Archivos:**
- `index.html` - Página principal
- `static/css/styles.css` - Estilos
- `static/js/app.js` - Lógica JavaScript
- `server.py` - Servidor de desarrollo
- `test_frontend.py` - Tests

**Funciones JavaScript:**
- `predictChurn()` - Envía request a la API
- `getFormData()` - Obtiene datos del formulario
- `displayResult()` - Muestra resultados
- `validateFormData()` - Valida entrada

**¿Cuándo usar?**
- ✅ Necesitas una interfaz para el usuario final
- ✅ Quieres personalizar el diseño
- ✅ Buscas agregar nuevas funcionalidades al frontend
- ✅ Necesitas probar la integración con la API

---

### 📈 Reports & Visualizations

**Archivo:** [reports/README.md](../reports/README.md)

**Contenido:**
- 📊 Reportes de deployment
- 📈 Visualizaciones de métricas
- 🔍 Gráficos de drift
- 📝 Logs de ejecución

**Subcarpetas:**
- `deployment/` - Reportes de despliegue
  - `DEPLOYMENT_REPORT.md`
  - `SUMMARY.md`
- `plots/` - Visualizaciones
  - `confusion_matrices/` - Matrices de confusión
  - `roc_curves/` - Curvas ROC
  - `feature_importance/` - Importancia de features
  - `drift_detection/` - Gráficos de drift
  - `eda/` - Gráficos de EDA
- `logs/` - Logs (opcional)
  - `training.log`
  - `api.log`
  - `monitoring.log`

**¿Cuándo usar?**
- ✅ Necesitas generar reportes de resultados
- ✅ Quieres visualizar métricas del modelo
- ✅ Buscas documentar el deployment
- ✅ Necesitas analizar logs del sistema

---

## 🗺️ Guías de Navegación por Caso de Uso

### 🎓 Caso 1: Soy nuevo en el proyecto

**Ruta recomendada:**
1. 📖 [README Principal](./README_PRINCIPAL.md) - Visión general
2. 🚀 Quick Start - Ejecutar el proyecto completo
3. 🔍 [README EDA](./README_EDA.md) - Entender los datos
4. 🔧 [README Feature Engineering](./README_FEATURE_ENGINEERING.md) - Preprocesamiento
5. 🤖 [README Model Training](./README_MODEL_TRAINING.md) - Modelos

---

### 🛠️ Caso 2: Quiero modificar el pipeline de ML

**Ruta recomendada:**
1. 🔧 [README Feature Engineering](./README_FEATURE_ENGINEERING.md) - Modificar preprocesamiento
2. 🤖 [README Model Training](./README_MODEL_TRAINING.md) - Agregar/modificar modelos
3. 📈 [README Reports](../reports/README.md) - Ver resultados

**Archivos a editar:**
- `mlops_pipeline/src/ft_engineering.py` - Pipelines
- `mlops_pipeline/src/model_training_evaluation.py` - Modelos

---

### 🚀 Caso 3: Quiero deployar en producción

**Ruta recomendada:**
1. 🚀 [README Deployment](./README_DEPLOYMENT.md) - API REST
2. 🐳 [Docker README](../docker/README.md) - Containerización
3. 🎨 [Frontend README](../frontend/README.md) - Interfaz de usuario

**Comandos clave:**
```powershell
# Con Docker
docker-compose -f docker/docker-compose.yml up -d

# Sin Docker
python -m mlops_pipeline.src.model_deploy
streamlit run mlops_pipeline/src/streamlit_app.py
```

---

### 📊 Caso 4: Quiero monitorear el modelo

**Ruta recomendada:**
1. 📊 [README Monitoring](./README_MONITORING.md) - Drift detection
2. 📈 [README Reports](../reports/README.md) - Visualizaciones

**Comandos clave:**
```powershell
# Ejecutar detección de drift
python -m mlops_pipeline.src.model_monitoring

# Ver dashboard
streamlit run mlops_pipeline/src/streamlit_app.py
```

---

### 🔧 Caso 5: Quiero agregar un nuevo modelo

**Pasos:**
1. Leer [README Model Training](./README_MODEL_TRAINING.md)
2. Modificar `model_training_evaluation.py`:
   - Agregar modelo en `build_models()` (línea ~122)
   - El resto del código ya maneja automáticamente el nuevo modelo
3. Ejecutar entrenamiento:
   ```powershell
   python -m mlops_pipeline.src.model_training_evaluation
   ```
4. Verificar resultados en `reports/plots/`

---

### 🐛 Caso 6: Tengo un error y necesito debuggear

**Dependiendo del error:**

**Error en entrenamiento:**
- 🤖 [README Model Training](./README_MODEL_TRAINING.md) - Troubleshooting
- 🔧 [README Feature Engineering](./README_FEATURE_ENGINEERING.md) - Si falla el preprocessor

**Error en API:**
- 🚀 [README Deployment](./README_DEPLOYMENT.md) - Troubleshooting API
- 🐳 [Docker README](../docker/README.md) - Si usas Docker

**Error en drift detection:**
- 📊 [README Monitoring](./README_MONITORING.md) - Troubleshooting

**Error de datos:**
- 💾 [Data README](../data/README.md) - Verificar estructura de datos

---

## 🔍 Búsqueda Rápida

### Por Función

| Función | Archivo | Línea | Documentación |
|---------|---------|-------|---------------|
| `build_preprocessor()` | ft_engineering.py | ~157 | [Feature Engineering](./README_FEATURE_ENGINEERING.md) |
| `train_with_cross_validation()` | model_training_evaluation.py | ~159 | [Model Training](./README_MODEL_TRAINING.md) |
| `calculate_psi()` | model_monitoring.py | ~75 | [Monitoring](./README_MONITORING.md) |
| `predict()` endpoint | model_deploy.py | ~145 | [Deployment](./README_DEPLOYMENT.md) |
| `validate_input_data()` | model_deploy.py | ~82 | [Deployment](./README_DEPLOYMENT.md) |

### Por Artefacto

| Artefacto | Ubicación | Documentación |
|-----------|-----------|---------------|
| `best_model.pkl` | models/ | [Models README](../models/README.md) |
| `preprocessor.pkl` | models/ | [Models README](../models/README.md) |
| `train_data.csv` | data/processed/ | [Data README](../data/README.md) |
| `drift_report.json` | data/metadata/ | [Monitoring](./README_MONITORING.md) |

### Por Endpoint

| Endpoint | Método | Documentación |
|----------|--------|---------------|
| `/predict` | POST | [Deployment](./README_DEPLOYMENT.md) |
| `/model-info` | GET | [Deployment](./README_DEPLOYMENT.md) |
| `/` (health check) | GET | [Deployment](./README_DEPLOYMENT.md) |

---

## 📊 Mapeo de Checklist del Proyecto

Todos los requisitos del "Checklist PROYECTO FINAL MACHINE LEARNING" están documentados con referencias exactas a archivos y líneas de código en:

🎯 **[README Principal - Sección Checklist](./README_PRINCIPAL.md#requisitos-del-checklist---mapeo-completo)**

---

## 🔗 Enlaces Directos

### Documentación Principal
- 📖 [README Principal](./README_PRINCIPAL.md)
- 📑 Este índice

### Módulos MLOps
- 🔍 [EDA](./README_EDA.md)
- 🔧 [Feature Engineering](./README_FEATURE_ENGINEERING.md)
- 🤖 [Model Training](./README_MODEL_TRAINING.md)
- 🚀 [Deployment](./README_DEPLOYMENT.md)
- 📊 [Monitoring](./README_MONITORING.md)

### Infraestructura
- 🐳 [Docker](../docker/README.md)
- 💾 [Data](../data/README.md)
- 🎯 [Models](../models/README.md)
- 🎨 [Frontend](../frontend/README.md)
- 📈 [Reports](../reports/README.md)

### Recursos Externos
- [Repositorio GitHub](https://github.com/MiguelRodriguez09/Final-ML---Dspliegue-MLOps)
- [Scikit-learn Docs](https://scikit-learn.org/)
- [Flask Docs](https://flask.palletsprojects.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Docker Docs](https://docs.docker.com/)

---

## 🎯 Checklist de Documentación Completa

Todos los documentos requeridos:

- ✅ **README_PRINCIPAL.md** - Visión general y mapeo de checklist
- ✅ **README_EDA.md** - Análisis exploratorio
- ✅ **README_FEATURE_ENGINEERING.md** - Preprocesamiento
- ✅ **README_MODEL_TRAINING.md** - Entrenamiento y evaluación
- ✅ **README_DEPLOYMENT.md** - API y deployment
- ✅ **README_MONITORING.md** - Detección de drift
- ✅ **INDICE_DOCUMENTACION.md** - Este archivo
- ✅ **docker/README.md** - Containerización
- ✅ **data/README.md** - Estructura de datos
- ✅ **models/README.md** - Artefactos del modelo
- ✅ **frontend/README.md** - Interfaz web
- ✅ **reports/README.md** - Reportes y visualizaciones

---

## 💡 Tips de Navegación

### Para evaluadores:
1. Empezar por [README Principal](./README_PRINCIPAL.md) para visión general
2. Verificar el mapeo de checklist en la sección correspondiente
3. Navegar a documentación específica según el requisito a evaluar
4. Todas las referencias incluyen archivos y números de línea aproximados

### Para desarrolladores:
1. Identificar el módulo que necesitas modificar
2. Ir a la documentación correspondiente
3. Seguir las instrucciones de ejecución
4. Verificar la sección de troubleshooting si hay errores

### Para nuevos miembros del equipo:
1. Leer [README Principal](./README_PRINCIPAL.md) completo
2. Seguir el Quick Start para ejecutar el proyecto
3. Explorar cada módulo en orden (EDA → FE → Training → Deployment → Monitoring)
4. Experimentar con modificaciones pequeñas

---

## 🆘 ¿Necesitas Ayuda?

**Si no encuentras lo que buscas:**

1. **Busca en este índice** por palabra clave
2. **Revisa el README Principal** - Tiene el mapeo completo
3. **Consulta el módulo específico** - Cada README tiene sección de troubleshooting
4. **Verifica los comentarios en el código** - Están bien documentados
5. **Abre un issue en GitHub** - Para preguntas técnicas

---

**Última actualización:** 2024
**Versión de documentación:** 1.0.0
