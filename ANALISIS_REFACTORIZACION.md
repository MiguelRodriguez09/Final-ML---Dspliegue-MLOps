# 📋 ANÁLISIS DE REFACTORIZACIÓN - MLOps Pipeline

## 🎯 Objetivo
Analizar y documentar **todos** los archivos que necesitan modificación de rutas tras la refactorización de la estructura de carpetas, sin cambiar ninguna línea de lógica de negocio.

---

## 📊 ESTRUCTURA ACTUAL DEL PROYECTO

```
Proyecto/
├── mlops_pipeline/
│   └── src/
│       ├── streamlit_app.py
│       ├── model_training_evaluation.py
│       ├── model_monitoring.py
│       ├── model_deploy.py
│       ├── ft_engineering.py
│       └── __pycache__/
├── frontend/
│   ├── server.py
│   ├── index.html
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
├── data/
│   ├── raw/Churn_Modelling.csv
│   ├── processed/
│   └── metadata/
├── models/
│   ├── config.json
│   └── model_metadata.json
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Dockerfile.frontend
│   └── Dockerfile.streamlit
├── scripts/
│   ├── start_all.bat
│   ├── start_frontend.bat
│   └── run_pipeline.bat
├── reports/
├── docs/
└── [archivos raíz]
    ├── best_model.pkl
    ├── preprocessor.pkl
    ├── model_metadata.json
    ├── train_data.csv
    ├── test_data.csv
    ├── drift_report.json
    └── eda_metadata.json
```

---

## 🔍 ANÁLISIS DETALLADO DE ARCHIVOS A MODIFICAR

### 1️⃣ **ARCHIVOS PYTHON - Módulos MLOps Pipeline**

#### **Archivo: `mlops_pipeline/src/streamlit_app.py`**
**Líneas a modificar:**

**Línea 30:**
```python
# ACTUAL:
from mlops_pipeline.src.model_monitoring import DriftMonitor

# PROBLEMA: Import relativo usando estructura de paquete completa
# ACCIÓN: Verificar si esta ruta funcionará después del movimiento
```

**Línea 23:**
```python
# ACTUAL:
project_root = Path(__file__).resolve().parent.parent.parent

# PROBLEMA: Navegación de directorios relativa
# EXPLICACIÓN: De streamlit_app.py -> src -> mlops_pipeline -> Proyecto (raíz)
# ACCIÓN: Verificar que esta ruta siga siendo correcta según nueva estructura
```

**Impacto:** Alto - Este archivo es el dashboard principal de Streamlit

---

#### **Archivo: `mlops_pipeline/src/model_deploy.py`**
**Líneas a modificar:**

**Línea 38:**
```python
# ACTUAL:
PROJECT_ROOT = Path(__file__).parent.parent.parent

# PROBLEMA: Navegación relativa para encontrar la raíz
# EXPLICACIÓN: De model_deploy.py -> src -> mlops_pipeline -> Proyecto (raíz)
# ACCIÓN: Verificar corrección tras movimiento
```

**Líneas de carga de archivos (aproximadamente 45-60):**
```python
# RUTAS DE CARGA DE ARTEFACTOS:
# - MODEL: best_model.pkl
# - PREPROCESSOR: preprocessor.pkl  
# - FEATURE_NAMES: feature_engineering_metadata.json
# - MODEL_METADATA: model_metadata.json

# ACCIÓN: Revisar todas las rutas de carga en la función load_artifacts()
```

**Impacto:** CRÍTICO - API Flask para predicciones, fallo rompe el servicio

---

#### **Archivo: `mlops_pipeline/src/model_monitoring.py`**
**Líneas a revisar:**

**Constructor `__init__` (línea ~48-54):**
```python
# Probablemente usa project_root para cargar:
# - train_data.csv (datos de referencia)
# - drift_report.json (reportes anteriores)

# ACCIÓN: Revisar constructor y métodos de carga
```

**Impacto:** Alto - Sistema de monitoreo de drift

---

#### **Archivo: `mlops_pipeline/src/ft_engineering.py`**
**Líneas a modificar:**

**Línea 71-75 (método `_load_metadata`):**
```python
# ACTUAL:
metadata_path = self.project_root / 'eda_metadata.json'

# PROBLEMA: Archivo en raíz, debería estar en data/metadata/
# ACCIÓN: Actualizar ruta a: data/metadata/eda_metadata.json
```

**Línea 86-91 (método `load_data`):**
```python
# ACTUAL:
data_path = self.project_root / 'data_cleaned.csv'
# FALLBACK:
data_path = self.project_root / 'Churn_Modelling.csv'

# PROBLEMA: Rutas incorrectas
# ACCIÓN: Actualizar a:
# - data/processed/data_cleaned.csv
# - data/raw/Churn_Modelling.csv
```

**Impacto:** Alto - Procesamiento de características

---

#### **Archivo: `mlops_pipeline/src/model_training_evaluation.py`**
**Líneas a revisar:**

Buscar patrones de carga de:
- `train_data.csv` → debe ser `data/processed/train_data.csv`
- `test_data.csv` → debe ser `data/processed/test_data.csv`
- Guardado de `best_model.pkl` → debe ir a `models/best_model.pkl`
- Guardado de `preprocessor.pkl` → debe ir a `models/preprocessor.pkl`

**Impacto:** CRÍTICO - Entrenamiento y evaluación de modelos

---

### 2️⃣ **ARCHIVOS FRONTEND**

#### **Archivo: `frontend/index.html`**
**Líneas a modificar:**

**Línea 7:**
```html
<!-- ACTUAL: -->
<link rel="stylesheet" href="static/css/styles.css">

<!-- ESTADO: Correcto (ruta relativa desde index.html)
<!-- ACCIÓN: Mantener si index.html permanece en frontend/ -->
```

**Línea 373:**
```html
<!-- ACTUAL: -->
<script src="static/js/app.js"></script>

<!-- ESTADO: Correcto (ruta relativa)
<!-- ACCIÓN: Mantener si index.html permanece en frontend/ -->
```

**Impacto:** Bajo - Solo si se mueve index.html

---

#### **Archivo: `frontend/static/js/app.js`**
**Líneas a modificar:**

**Líneas 6-9:**
```javascript
// ACTUAL:
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'  // Desarrollo local
    : 'http://localhost:5000';  // Producción

// PROBLEMA: Hardcoded, pero podría necesitar variable de entorno
// ACCIÓN: Considerar usar variable de entorno para Docker
```

**Línea 150:**
```javascript
// ACTUAL:
const response = await fetch(`${API_BASE_URL}${endpoint}`, {

// ESTADO: Correcto (usa variable API_BASE_URL)
// ACCIÓN: Mantener, verificar que API_BASE_URL esté correcta
```

**Impacto:** Medio - Comunicación Frontend-API

---

#### **Archivo: `frontend/server.py`**
**Líneas a modificar:**

**Línea 41:**
```python
# ACTUAL:
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ESTADO: Correcto (cambia al directorio del script)
# ACCIÓN: Mantener, funciona independientemente de la ubicación
```

**Impacto:** Bajo - Servidor estático simple

---

### 3️⃣ **ARCHIVOS DOCKER**

#### **Archivo: `docker/docker-compose.yml`**
**Líneas a modificar:**

**Líneas 16-22 (servicio api):**
```yaml
# ACTUAL:
context: .
dockerfile: Dockerfile

# PROBLEMA: Context incorrecto si docker-compose.yml está en docker/
# ACCIÓN: 
# Opción 1: Mover docker-compose.yml a raíz
# Opción 2: Cambiar context a: context: ..
```

**Líneas 27-30 (volúmenes API):**
```yaml
# ACTUAL:
- ./best_model.pkl:/app/best_model.pkl:ro
- ./preprocessor.pkl:/app/preprocessor.pkl:ro
- ./model_metadata.json:/app/model_metadata.json:ro

# PROBLEMA: Rutas relativas desde ubicación de docker-compose.yml
# ACCIÓN: Si docker-compose.yml está en docker/:
# - ../models/best_model.pkl:/app/best_model.pkl:ro
# - ../models/preprocessor.pkl:/app/preprocessor.pkl:ro
# - ../models/model_metadata.json:/app/model_metadata.json:ro
```

**Líneas 62-66 (volúmenes Dashboard):**
```yaml
# ACTUAL:
- ./train_data.csv:/app/train_data.csv:ro
- ./test_data.csv:/app/test_data.csv:ro
- ./drift_report.json:/app/drift_report.json:ro

# PROBLEMA: Archivos deben estar en data/
# ACCIÓN:
# - ../data/processed/train_data.csv:/app/train_data.csv:ro
# - ../data/processed/test_data.csv:/app/test_data.csv:ro
# - ../data/metadata/drift_report.json:/app/drift_report.json:ro
```

**Líneas 76-80 (servicio frontend):**
```yaml
# ACTUAL:
build:
  context: .
  dockerfile: Dockerfile.frontend

# PROBLEMA: Context incorrecto
# ACCIÓN: Ajustar según ubicación de docker-compose.yml
```

**Impacto:** CRÍTICO - Orquestación de contenedores Docker

---

#### **Archivo: `docker/Dockerfile`**
**Líneas a revisar:**

Buscar:
- `COPY` statements que copien archivos desde rutas específicas
- `WORKDIR` definiciones
- `CMD` o `ENTRYPOINT` con rutas

**Ejemplo típico:**
```dockerfile
# Posible línea:
COPY mlops_pipeline/src/model_deploy.py /app/

# ACCIÓN: Verificar que las rutas COPY sean correctas
```

**Impacto:** Alto - Construcción de imagen Docker

---

#### **Archivo: `docker/Dockerfile.streamlit`**
**Líneas a revisar:**

Similar a Dockerfile, revisar:
- `COPY` de archivos del dashboard
- `CMD` para ejecutar streamlit_app.py

**Ejemplo:**
```dockerfile
# Posible línea:
CMD ["streamlit", "run", "mlops_pipeline/src/streamlit_app.py"]

# ACCIÓN: Verificar ruta correcta
```

**Impacto:** Alto - Construcción de imagen Streamlit

---

#### **Archivo: `docker/Dockerfile.frontend`**
**Líneas a revisar:**

```dockerfile
# Posibles líneas:
COPY frontend/ /app/
WORKDIR /app
CMD ["python", "server.py"]

# ACCIÓN: Verificar estructura de COPY
```

**Impacto:** Medio - Construcción de imagen Frontend

---

### 4️⃣ **SCRIPTS DE AUTOMATIZACIÓN**

#### **Archivo: `scripts/start_all.bat`**
**Líneas a modificar:**

**Línea 61:**
```bat
REM ACTUAL:
start "MLOps API" cmd /c "python mlops_pipeline/src/model_deploy.py"

REM PROBLEMA: Ruta relativa desde ubicación de ejecución
REM ACCIÓN: Asegurar que se ejecuta desde raíz o usar ruta absoluta
```

**Línea 74:**
```bat
REM ACTUAL:
cd frontend
start "MLOps Frontend" cmd /c "python server.py"
cd ..

REM ESTADO: Correcto si frontend/ sigue en raíz
REM ACCIÓN: Verificar tras movimiento
```

**Impacto:** Alto - Script principal de inicio

---

#### **Archivo: `scripts/start_frontend.bat`**
**Líneas a revisar:**

Buscar:
- Cambios de directorio (`cd`)
- Ejecución de `python server.py`
- Referencias a rutas de frontend

**Impacto:** Medio - Script de frontend

---

#### **Archivo: `scripts/run_pipeline.bat`**
**Líneas a revisar:**

Buscar:
- Ejecución de scripts Python del pipeline
- Rutas a archivos de datos
- Rutas a notebooks

**Ejemplo probable:**
```bat
python mlops_pipeline/src/ft_engineering.py
python mlops_pipeline/src/model_training_evaluation.py
```

**Impacto:** Alto - Script de pipeline completo

---

#### **Archivo: `scripts/QUICK_START.bat`**
**Líneas a revisar:**

Similar a start_all.bat, buscar:
- Rutas de ejecución
- Cambios de directorio
- Referencias a archivos

**Impacto:** Medio - Script de inicio rápido

---

### 5️⃣ **ARCHIVOS DE CONFIGURACIÓN**

#### **Archivo: `Makefile`**
**Líneas a modificar:**

**Línea 25:**
```makefile
# ACTUAL:
$(DOCKER_COMPOSE) build --no-cache

# PROBLEMA: Si docker-compose.yml está en docker/, necesita:
# ACCIÓN: Agregar -f flag:
# $(DOCKER_COMPOSE) -f docker/docker-compose.yml build --no-cache
```

**Todas las líneas con `$(DOCKER_COMPOSE)`:**
```makefile
# ACCIÓN: Agregar -f docker/docker-compose.yml si se mueve docker-compose.yml
```

**Impacto:** Alto - Comandos Make para Docker

---

#### **Archivo: `sonar-project.properties`**
**Líneas a revisar:**

```properties
# Posibles líneas:
# sonar.sources=mlops_pipeline/src
# sonar.python.coverage.reportPaths=coverage.xml

# ACCIÓN: Verificar rutas de análisis de código
```

**Impacto:** Bajo - Análisis de código estático

---

#### **Archivo: `requirements.txt`**
**Estado:** No requiere cambios (solo lista de dependencias)

**Impacto:** Ninguno

---

### 6️⃣ **ARCHIVOS DE DATOS Y METADATOS**

**NOTA IMPORTANTE:** Estos archivos **NO CONTIENEN CÓDIGO**, pero su **ubicación** afecta las rutas en el código Python.

**Archivos afectados:**
- `best_model.pkl` → Mover a `models/`
- `preprocessor.pkl` → Mover a `models/`
- `train_data.csv` → Mover a `data/processed/`
- `test_data.csv` → Mover a `data/processed/`
- `data_cleaned.csv` → Mover a `data/processed/`
- `drift_report.json` → Mover a `data/metadata/`
- `eda_metadata.json` → Mover a `data/metadata/`
- `feature_engineering_metadata.json` → Mover a `data/metadata/`

**Impacto:** CRÍTICO - Todos los módulos Python dependen de estas rutas

---

## 🎯 RESUMEN DE PRIORIDADES

### 🔴 **PRIORIDAD CRÍTICA (Rompen funcionalidad)**
1. `mlops_pipeline/src/model_deploy.py` - API Flask
2. `mlops_pipeline/src/model_training_evaluation.py` - Entrenamiento
3. `docker/docker-compose.yml` - Orquestación Docker
4. Movimiento de archivos PKL y CSV a nuevas ubicaciones

### 🟡 **PRIORIDAD ALTA (Impactan funcionalidad)**
1. `mlops_pipeline/src/streamlit_app.py` - Dashboard
2. `mlops_pipeline/src/ft_engineering.py` - Feature Engineering
3. `mlops_pipeline/src/model_monitoring.py` - Monitoreo
4. `scripts/start_all.bat` - Script principal
5. `Makefile` - Comandos Docker

### 🟢 **PRIORIDAD MEDIA (Pueden fallar)**
1. `docker/Dockerfile` - Build de API
2. `docker/Dockerfile.streamlit` - Build de Dashboard
3. `frontend/static/js/app.js` - API URL
4. `scripts/run_pipeline.bat` - Pipeline completo

### ⚪ **PRIORIDAD BAJA (Mínimo impacto)**
1. `frontend/server.py` - Servidor estático
2. `sonar-project.properties` - Análisis de código
3. Scripts adicionales en `scripts/`

---

## 📝 CHECKLIST DE VERIFICACIÓN

Después de realizar los cambios, verificar:

- [ ] ✅ La API Flask inicia correctamente (`python mlops_pipeline/src/model_deploy.py`)
- [ ] ✅ El Dashboard Streamlit carga sin errores (`streamlit run mlops_pipeline/src/streamlit_app.py`)
- [ ] ✅ El Frontend conecta con la API correctamente
- [ ] ✅ Docker Compose construye todas las imágenes (`docker-compose build`)
- [ ] ✅ Docker Compose levanta todos los servicios (`docker-compose up`)
- [ ] ✅ Los scripts .bat ejecutan correctamente
- [ ] ✅ El Makefile ejecuta comandos sin errores
- [ ] ✅ Todos los archivos de datos están en las ubicaciones correctas
- [ ] ✅ Los modelos .pkl se cargan correctamente
- [ ] ✅ Los metadatos JSON se leen correctamente

---

## 🚀 PLAN DE ACCIÓN RECOMENDADO

### **FASE 1: PREPARACIÓN**
1. Crear backup completo del proyecto
2. Crear nueva estructura de carpetas vacía
3. Documentar estructura actual vs. nueva

### **FASE 2: MOVIMIENTO DE ARCHIVOS**
1. Mover archivos de datos a `data/processed/` y `data/metadata/`
2. Mover archivos de modelo a `models/`
3. Verificar que no se movieron archivos de código

### **FASE 3: ACTUALIZACIÓN DE RUTAS EN CÓDIGO**
1. Actualizar rutas en `ft_engineering.py`
2. Actualizar rutas en `model_deploy.py`
3. Actualizar rutas en `model_training_evaluation.py`
4. Actualizar rutas en `streamlit_app.py`
5. Actualizar rutas en `model_monitoring.py`

### **FASE 4: ACTUALIZACIÓN DE DOCKER**
1. Ajustar `docker-compose.yml` (rutas de volúmenes y contexto)
2. Verificar `Dockerfile`, `Dockerfile.streamlit`, `Dockerfile.frontend`
3. Actualizar `Makefile` si es necesario

### **FASE 5: ACTUALIZACIÓN DE SCRIPTS**
1. Actualizar `start_all.bat`
2. Actualizar otros scripts en `scripts/`

### **FASE 6: TESTING**
1. Ejecutar cada script individualmente
2. Probar API localmente
3. Probar Dashboard localmente
4. Probar con Docker
5. Verificar checklist completo

---

## 📌 NOTAS IMPORTANTES

1. **NO CAMBIAR LÓGICA:** Solo modificar declaraciones de rutas (import, Path, volúmenes)
2. **RUTAS RELATIVAS:** Preferir rutas relativas usando `Path(__file__).parent`
3. **DOCKER:** Considerar diferencias entre rutas locales y rutas dentro del contenedor
4. **TESTING:** Probar cada cambio de forma aislada antes de continuar
5. **BACKUP:** Mantener backup hasta confirmar que todo funciona

---

## ❓ PREGUNTAS PARA CLARIFICAR

Antes de proceder, necesitas definir:

1. **¿Cuál es la NUEVA estructura de carpetas propuesta?**
2. **¿Se moverá `docker-compose.yml` a la raíz o permanece en `docker/`?**
3. **¿Los Dockerfiles permanecen en `docker/`?**
4. **¿Hay cambios en la estructura de `mlops_pipeline/`?**
5. **¿Se reorganiza la carpeta `frontend/`?**

---

**Fecha de análisis:** ${new Date().toLocaleDateString()}  
**Tecnologías:** Python, Flask, Streamlit, Docker, JavaScript  
**Total de archivos identificados:** ~20+  
**Nivel de complejidad:** Alto
