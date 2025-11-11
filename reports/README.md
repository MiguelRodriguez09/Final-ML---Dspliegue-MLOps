# Carpeta: Reports

## 1. Propósito

Esta carpeta contiene los **reportes y visualizaciones** generados durante el ciclo de vida del modelo:
- Reportes de deployment
- Gráficos de evaluación
- Métricas de monitoreo
- Logs de ejecución
- Documentación de resultados

---

## 2. Estructura de la Carpeta

```
reports/
├── deployment/                # Reportes de despliegue
│   ├── DEPLOYMENT_REPORT.md  # Reporte detallado del deployment
│   └── SUMMARY.md             # Resumen ejecutivo
├── plots/                     # Visualizaciones generadas
│   ├── confusion_matrices/    # Matrices de confusión por modelo
│   ├── roc_curves/            # Curvas ROC
│   ├── feature_importance/    # Importancia de features
│   ├── drift_detection/       # Gráficos de drift
│   └── eda/                   # Gráficos de EDA
└── logs/                      # Logs de ejecución (si aplica)
    ├── training.log           # Logs de entrenamiento
    ├── api.log                # Logs de la API
    └── monitoring.log         # Logs de monitoreo
```

---

## 3. Descripción de Subcarpetas

### 3.1. `deployment/`

**Propósito:** Documentación del proceso de despliegue.

#### 3.1.1. `DEPLOYMENT_REPORT.md`

**Contenido esperado:**
```markdown
# Reporte de Deployment - MLOps Churn Prediction

## 1. Información General
- **Fecha de deployment:** 2024-01-15
- **Versión del modelo:** v1.2.3
- **Ambiente:** Production
- **Responsable:** [Nombre del equipo]

## 2. Configuración
- **Framework:** Flask 3.0.0
- **Puerto:** 5000
- **Containerización:** Docker
- **Orquestación:** Docker Compose
- **Base de datos:** No aplica (modelo sin estado)

## 3. Artefactos Deployados
- `best_model.pkl` (15.2 MB)
- `preprocessor.pkl` (45 KB)
- `model_metadata.json` (2 KB)

## 4. Tests de Deployment
- ✅ Health check endpoint
- ✅ Prediction endpoint (single)
- ✅ Prediction endpoint (batch)
- ✅ Model info endpoint
- ✅ Load testing (1000 requests/min)

## 5. Métricas de Performance
- **Latencia promedio:** 150ms
- **Throughput:** 800 req/min
- **Memoria utilizada:** 512 MB
- **CPU utilizado:** 15%

## 6. Problemas Encontrados
- Ninguno

## 7. Próximos Pasos
- Implementar monitoreo con Prometheus
- Configurar alertas con Grafana
- Implementar CI/CD con GitHub Actions
```

#### 3.1.2. `SUMMARY.md`

**Contenido esperado:**
```markdown
# Resumen Ejecutivo - Deployment MLOps

## ✅ Estado
**EXITOSO** - Modelo deployado en producción

## 📊 Métricas Clave
- Accuracy: 86.5%
- Latencia: 150ms
- Uptime: 99.9%

## 🚀 Próximos Pasos
1. Monitoreo continuo
2. Reentrenamiento mensual
3. A/B testing de nuevos modelos
```

---

### 3.2. `plots/`

**Propósito:** Visualizaciones generadas por los scripts de entrenamiento y monitoreo.

#### 3.2.1. Subdirectorio: `confusion_matrices/`

**Archivos generados por:** `model_training_evaluation.py` → `plot_confusion_matrices()`

**Archivos típicos:**
```
confusion_matrices/
├── confusion_matrix_logistic_regression.png
├── confusion_matrix_decision_tree.png
├── confusion_matrix_random_forest.png
└── confusion_matrix_gradient_boosting.png
```

**Ubicación en código:**
```python
# mlops_pipeline/src/model_training_evaluation.py
# Línea ~444-500
def plot_confusion_matrices(self, results):
    """
    Guarda matrices de confusión en reports/plots/confusion_matrices/
    """
    for model_name, result in results.items():
        output_path = f'reports/plots/confusion_matrices/confusion_matrix_{model_name}.png'
        # ... código para generar y guardar el plot
```

**Información en el gráfico:**
- True Positives, True Negatives
- False Positives, False Negatives
- Accuracy por modelo

---

#### 3.2.2. Subdirectorio: `roc_curves/`

**Archivos generados por:** `model_training_evaluation.py` → `plot_roc_curves()`

**Archivos típicos:**
```
roc_curves/
├── roc_curves_comparison.png      # Comparación de todos los modelos
├── roc_curve_logistic_regression.png
├── roc_curve_decision_tree.png
├── roc_curve_random_forest.png
└── roc_curve_gradient_boosting.png
```

**Ubicación en código:**
```python
# mlops_pipeline/src/model_training_evaluation.py
# Línea ~393-443
def plot_roc_curves(self, results):
    """
    Guarda curvas ROC en reports/plots/roc_curves/
    """
    output_path = 'reports/plots/roc_curves/roc_curves_comparison.png'
    # ... código para generar el plot comparativo
```

**Información en el gráfico:**
- Curvas ROC de cada modelo
- AUC (Area Under Curve) de cada modelo
- Línea diagonal de referencia (clasificador aleatorio)

---

#### 3.2.3. Subdirectorio: `feature_importance/`

**Archivos generados por:** `model_training_evaluation.py` → `plot_feature_importance()`

**Archivos típicos:**
```
feature_importance/
├── feature_importance_random_forest.png
├── feature_importance_gradient_boosting.png
└── feature_importance_comparison.png
```

**Información en el gráfico:**
- Top 10-20 features más importantes
- Score de importancia normalizado
- Comparación entre modelos tree-based

**Ejemplo de uso:**
```python
# En model_training_evaluation.py
trainer = ModelTrainer()
results = trainer.train_with_cross_validation(X_train, y_train)
trainer.plot_feature_importance(results)
```

---

#### 3.2.4. Subdirectorio: `drift_detection/`

**Archivos generados por:** `model_monitoring.py` → `DriftMonitor.plot_drift_distributions()`

**Archivos típicos:**
```
drift_detection/
├── drift_CreditScore.png          # Distribución baseline vs production
├── drift_Age.png
├── drift_Balance.png
├── drift_Geography.png
├── drift_Gender.png
└── drift_summary.png               # Resumen de todas las features
```

**Ubicación en código:**
```python
# mlops_pipeline/src/model_monitoring.py
# Línea ~335-400 (aproximado)
def plot_drift_distributions(self, baseline_data, production_data):
    """
    Guarda gráficos de distribución en reports/plots/drift_detection/
    """
    for column in baseline_data.columns:
        output_path = f'reports/plots/drift_detection/drift_{column}.png'
        # ... código para comparar distribuciones
```

**Información en el gráfico:**
- Distribución baseline (train data)
- Distribución production (new data)
- PSI score
- Alertas de drift detectado

---

#### 3.2.5. Subdirectorio: `eda/`

**Archivos generados por:** `compresion_eda.ipynb` o scripts de EDA

**Archivos típicos:**
```
eda/
├── age_distribution.png
├── balance_by_geography.png
├── churn_rate_by_age.png
├── correlation_matrix.png
├── numerical_features_distribution.png
└── categorical_features_distribution.png
```

**Información típica:**
- Distribuciones univariadas
- Correlaciones entre features
- Análisis de target (churn)
- Outliers detectados

---

### 3.3. `logs/` (Opcional)

**Propósito:** Logs de ejecución del sistema.

#### 3.3.1. `training.log`

**Generado por:** `model_training_evaluation.py` con configuración de logging

**Formato típico:**
```
2024-01-15 10:30:15 INFO - Iniciando entrenamiento de modelos
2024-01-15 10:30:16 INFO - Cargando datos de entrenamiento: 8000 filas
2024-01-15 10:30:20 INFO - Entrenando Logistic Regression...
2024-01-15 10:30:25 INFO - Logistic Regression - Accuracy: 0.798 (+/- 0.015)
2024-01-15 10:30:25 INFO - Entrenando Random Forest...
2024-01-15 10:32:10 INFO - Random Forest - Accuracy: 0.865 (+/- 0.012)
2024-01-15 10:32:11 INFO - Mejor modelo: Random Forest
2024-01-15 10:32:11 INFO - Guardando modelo en models/best_model.pkl
```

#### 3.3.2. `api.log`

**Generado por:** `model_deploy.py` con configuración de logging

**Formato típico:**
```
2024-01-15 14:00:00 INFO - API iniciada en puerto 5000
2024-01-15 14:05:23 INFO - POST /predict - 200 - 120ms
2024-01-15 14:05:45 INFO - POST /predict - 200 - 135ms
2024-01-15 14:06:12 ERROR - POST /predict - 400 - Campo faltante: Age
2024-01-15 14:10:30 INFO - GET /model-info - 200 - 5ms
```

#### 3.3.3. `monitoring.log`

**Generado por:** `model_monitoring.py` con configuración de logging

**Formato típico:**
```
2024-01-15 16:00:00 INFO - Iniciando detección de drift
2024-01-15 16:00:05 INFO - Baseline data: 8000 filas
2024-01-15 16:00:05 INFO - Production data: 1500 filas
2024-01-15 16:00:10 WARNING - Drift detectado en CreditScore (PSI: 0.35)
2024-01-15 16:00:12 INFO - No drift en Age (PSI: 0.08)
2024-01-15 16:00:15 ERROR - Drift crítico en Geography (Chi2 p-value: 0.001)
2024-01-15 16:00:20 INFO - Reporte guardado en data/metadata/drift_report.json
```

---

## 4. Generación de Reportes

### 4.1. Desde el Entrenamiento

**Ejecutar pipeline de entrenamiento:**
```powershell
# Navegar a la raíz del proyecto
cd c:\Users\Asus\Desktop\Proyecto

# Activar entorno virtual
.\Proyecto-venv\Scripts\Activate.ps1

# Ejecutar entrenamiento (genera plots en reports/)
python -m mlops_pipeline.src.model_training_evaluation
```

**Resultados esperados:**
- `reports/plots/confusion_matrices/*.png`
- `reports/plots/roc_curves/*.png`
- `reports/plots/feature_importance/*.png`

---

### 4.2. Desde el Monitoreo

**Ejecutar monitoreo de drift:**
```powershell
# Activar entorno virtual
.\Proyecto-venv\Scripts\Activate.ps1

# Ejecutar monitoreo (genera plots en reports/)
python -m mlops_pipeline.src.model_monitoring
```

**Resultados esperados:**
- `reports/plots/drift_detection/*.png`
- `data/metadata/drift_report.json`

**Visualizar en Streamlit:**
```powershell
streamlit run mlops_pipeline/src/streamlit_app.py
```

---

### 4.3. Desde EDA

**Ejecutar notebook de EDA:**
```powershell
# Iniciar Jupyter
jupyter notebook mlops_pipeline/src/compresion_eda.ipynb

# O ejecutar directamente
jupyter nbconvert --to notebook --execute mlops_pipeline/src/compresion_eda.ipynb
```

**Resultados esperados:**
- `reports/plots/eda/*.png`

---

## 5. Estructura de un Reporte Completo

### 5.1. Crear Reporte Manual

**Archivo:** `reports/deployment/DEPLOYMENT_REPORT.md`

**Plantilla:**
```markdown
# Reporte de Deployment - [Fecha]

## 1. Información del Modelo
- **Nombre:** Churn Prediction Model
- **Versión:** v1.0.0
- **Fecha de entrenamiento:** 2024-01-15
- **Accuracy:** 86.5%
- **AUC:** 0.89

## 2. Datos de Entrenamiento
- **Dataset:** Churn_Modelling.csv
- **Filas train:** 8000
- **Filas test:** 2000
- **Features:** 10
- **Clases:** 2 (Churn / No Churn)

## 3. Modelos Evaluados
| Modelo | Accuracy | Precision | Recall | F1-Score | AUC |
|--------|----------|-----------|--------|----------|-----|
| Logistic Regression | 0.798 | 0.76 | 0.52 | 0.62 | 0.82 |
| Decision Tree | 0.789 | 0.71 | 0.55 | 0.62 | 0.78 |
| Random Forest | **0.865** | **0.85** | **0.73** | **0.78** | **0.89** |
| Gradient Boosting | 0.862 | 0.84 | 0.72 | 0.77 | 0.88 |

## 4. Visualizaciones
Ver carpeta `reports/plots/`:
- Matrices de confusión
- Curvas ROC
- Importancia de features

## 5. Deployment
- **Ambiente:** Production
- **URL:** http://localhost:5000
- **Docker:** ✅
- **Health check:** ✅

## 6. Monitoreo
- **Dashboard:** http://localhost:8501
- **Drift detection:** Activo
- **Alertas:** Email configurado

## 7. Próximos Pasos
- [ ] Implementar reentrenamiento automático
- [ ] A/B testing con Gradient Boosting
- [ ] Optimizar hiperparámetros
```

---

## 6. Automatización de Reportes

### 6.1. Script de Generación Automática

**Crear:** `scripts/generate_report.py`

```python
"""
Script para generar reportes automáticamente.
"""

import json
from datetime import datetime
from pathlib import Path

def generate_deployment_report():
    """Generar reporte de deployment."""
    
    # Cargar metadata del modelo
    with open('models/model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Crear reporte
    report = f"""
# Reporte de Deployment - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Información del Modelo
- Nombre: {metadata['model_name']}
- Versión: {metadata['model_version']}
- Accuracy: {metadata['metrics']['accuracy']:.4f}
- AUC: {metadata['metrics']['roc_auc']:.4f}

## Estado
✅ Modelo deployado exitosamente

## Visualizaciones
- Matrices de confusión: reports/plots/confusion_matrices/
- Curvas ROC: reports/plots/roc_curves/
- Importancia features: reports/plots/feature_importance/
"""
    
    # Guardar reporte
    output_path = Path('reports/deployment/DEPLOYMENT_REPORT.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    
    print(f'✅ Reporte generado: {output_path}')

if __name__ == '__main__':
    generate_deployment_report()
```

**Uso:**
```powershell
python scripts/generate_report.py
```

---

## 7. Mejores Prácticas

### 7.1. Organización de Reportes

✅ **Hacer:**
- Usar timestamps en nombres de archivos
- Versionar reportes importantes
- Guardar plots con nombres descriptivos
- Incluir metadata en reportes

❌ **Evitar:**
- Sobrescribir reportes anteriores
- Nombres de archivo genéricos
- Mezclar reportes de diferentes experimentos

### 7.2. Versionado de Reportes

**Estrategia recomendada:**
```
reports/
├── deployment/
│   ├── 2024-01-15_DEPLOYMENT_REPORT.md
│   ├── 2024-02-01_DEPLOYMENT_REPORT.md
│   └── latest -> 2024-02-01_DEPLOYMENT_REPORT.md
├── plots/
│   ├── v1.0.0/
│   │   ├── confusion_matrices/
│   │   └── roc_curves/
│   └── v1.1.0/
│       ├── confusion_matrices/
│       └── roc_curves/
```

---

## 8. Integración con Git

### 8.1. `.gitignore` para Reports

**Agregar a `.gitignore`:**
```gitignore
# Reports grandes
reports/plots/**/*.png
reports/logs/*.log

# Mantener estructura
!reports/plots/.gitkeep
!reports/logs/.gitkeep

# Versionar reportes importantes
!reports/deployment/*.md
```

### 8.2. Git LFS para Plots Grandes

**Si los plots son importantes:**
```powershell
# Instalar Git LFS
git lfs install

# Track PNG files
git lfs track "reports/plots/**/*.png"

# Commit
git add .gitattributes
git add reports/plots/
git commit -m "Add training plots with Git LFS"
```

---

## 9. Visualización de Reportes

### 9.1. En Navegador

**Para Markdown:**
```powershell
# Con Python
python -m grip reports/deployment/DEPLOYMENT_REPORT.md

# O con VS Code
# Abrir archivo .md y presionar Ctrl+Shift+V
```

### 9.2. En Dashboard

**Con Streamlit:**
```python
# En streamlit_app.py
import streamlit as st
from pathlib import Path

# Mostrar reporte
report_path = Path('reports/deployment/DEPLOYMENT_REPORT.md')
if report_path.exists():
    st.markdown(report_path.read_text())

# Mostrar plots
st.image('reports/plots/roc_curves/roc_curves_comparison.png')
```

---

## 10. Troubleshooting

### Problema: Carpeta reports/plots vacía
**Causa:** Los scripts de entrenamiento/monitoreo no se han ejecutado.
**Solución:**
```powershell
# Ejecutar pipeline completo
python -m mlops_pipeline.src.model_training_evaluation
python -m mlops_pipeline.src.model_monitoring
```

### Problema: Plots no se generan
**Causa:** Carpetas de destino no existen.
**Solución:**
```powershell
# Crear estructura de carpetas
New-Item -ItemType Directory -Force -Path "reports\plots\confusion_matrices"
New-Item -ItemType Directory -Force -Path "reports\plots\roc_curves"
New-Item -ItemType Directory -Force -Path "reports\plots\feature_importance"
New-Item -ItemType Directory -Force -Path "reports\plots\drift_detection"
```

### Problema: Reportes no se actualizan
**Causa:** Cache de scripts o permisos de archivo.
**Solución:**
```powershell
# Limpiar cache
Remove-Item -Recurse -Force reports\plots\*

# Re-ejecutar
python -m mlops_pipeline.src.model_training_evaluation
```

---

## 11. Exportación de Reportes

### 11.1. A PDF

**Con pandoc:**
```powershell
# Instalar pandoc
choco install pandoc

# Convertir a PDF
pandoc reports/deployment/DEPLOYMENT_REPORT.md -o report.pdf
```

### 11.2. A HTML

**Con Python-Markdown:**
```python
import markdown
from pathlib import Path

md_file = Path('reports/deployment/DEPLOYMENT_REPORT.md')
html = markdown.markdown(md_file.read_text())

output_file = Path('reports/deployment/DEPLOYMENT_REPORT.html')
output_file.write_text(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Deployment Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 2rem; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
    </style>
</head>
<body>
    {html}
</body>
</html>
""")

print(f'✅ HTML generado: {output_file}')
```

---

## 12. Contacto

Para preguntas sobre reportes, referirse al README principal.

**Documentación relacionada:**
- [README Model Training](../docs/README_MODEL_TRAINING.md)
- [README Monitoring](../docs/README_MONITORING.md)
- [README Deployment](../docs/README_DEPLOYMENT.md)
