# 🚀 Guía de Inicio Rápido - MLOps Pipeline

## ⚡ Ejecución Rápida (5 minutos)

### 1. Configuración Inicial (Solo la primera vez)

```bash
# Windows
set_up.bat

# O manualmente:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ejecutar Pipeline Completo

```bash
# Windows - Modo Automatizado
run_pipeline.bat

# O paso a paso:
python mlops_pipeline/src/ft_engineering.py
python mlops_pipeline/src/model_training_evaluation.py
python mlops_pipeline/src/model_monitoring.py
```

### 3. Notebooks (EDA - Ejecutar ANTES del pipeline automatizado)

```bash
jupyter notebook mlops_pipeline/src/cargar_datos.ipynb
jupyter notebook mlops_pipeline/src/compresion_eda.ipynb
```

### 4. Iniciar Servicios

```bash
# API de Predicción (Terminal 1)
python mlops_pipeline/src/model_deploy.py

# Dashboard de Monitoreo (Terminal 2)
streamlit run mlops_pipeline/src/streamlit_app.py
```

---

## 📋 Orden Correcto de Ejecución

```
1. cargar_datos.ipynb          ← Cargar dataset
2. compresion_eda.ipynb        ← Análisis exploratorio
3. ft_engineering.py           ← Feature engineering
4. model_training_evaluation.py ← Entrenamiento
5. model_deploy.py             ← Despliegue (API)
6. model_monitoring.py         ← Análisis de drift
7. streamlit_app.py            ← Dashboard
```

---

## 🎯 Prueba Rápida de la API

```bash
# Health Check
curl http://localhost:5000/

# Información del Modelo
curl http://localhost:5000/model-info

# Predicción (Windows PowerShell)
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

## 🐳 Docker (Opcional)

```bash
# Construir
docker build -t mlops-api:latest .

# Ejecutar
docker run -d -p 5000:5000 --name mlops-api mlops-api:latest

# Verificar
curl http://localhost:5000/

# Detener
docker stop mlops-api && docker rm mlops-api
```

---

## 📊 Archivos Generados

Después de ejecutar el pipeline, encontrarás:

```
Proyecto/
├── data_cleaned.csv                    ← Dataset limpio (EDA)
├── eda_metadata.json                   ← Metadatos del EDA
├── train_data.csv                      ← Datos de entrenamiento
├── test_data.csv                       ← Datos de prueba
├── preprocessor.pkl                    ← Pipeline de transformación
├── feature_engineering_metadata.json   ← Metadatos de FE
├── best_model.pkl                      ← Mejor modelo entrenado
├── model_metadata.json                 ← Métricas del modelo
├── model_comparison.png                ← Comparación de modelos
├── confusion_matrices.png              ← Matrices de confusión
├── roc_curves.png                      ← Curvas ROC
├── drift_report.json                   ← Reporte de drift
└── drift_summary.png                   ← Visualización de drift
```

---

## ⚠️ Solución de Problemas Comunes

### Problema: Módulos no encontrados
```bash
# Solución: Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: Puerto 5000 en uso
```bash
# Solución: Cambiar puerto en model_deploy.py
# Línea final: app.run(host='0.0.0.0', port=5001)
```

### Problema: Archivos .pkl no encontrados
```bash
# Solución: Ejecutar en orden
python mlops_pipeline/src/ft_engineering.py
python mlops_pipeline/src/model_training_evaluation.py
# Luego intentar desplegar
```

### Problema: Jupyter no se abre
```bash
# Solución: Instalar Jupyter
pip install jupyter notebook
jupyter notebook
```

---

## 📖 Más Información

- **Documentación Completa**: Ver `README.md`
- **Resumen de Implementación**: Ver `SUMMARY.md`
- **Directrices del Proyecto**: Ver `Directrices/directriz_definitiva.md`

---

## 💡 Tips

1. **Siempre ejecutar los notebooks ANTES** del pipeline automatizado
2. **Verificar que exista `data_cleaned.csv`** antes de feature engineering
3. **El dashboard necesita `drift_report.json`** - ejecutar monitoreo primero
4. **Para reentrenar**: Ejecutar todo desde `ft_engineering.py`
5. **Para probar cambios**: Usar la rama `dev` primero

---

## ✅ Checklist de Verificación

- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Dataset `Churn_Modelling.csv` en la raíz
- [ ] Notebooks de EDA ejecutados
- [ ] Pipeline de FE ejecutado sin errores
- [ ] Modelos entrenados (verificar `best_model.pkl`)
- [ ] API responde en http://localhost:5000
- [ ] Dashboard abre en http://localhost:8501

---

¡Listo! 🎉 Tu pipeline MLOps está funcionando.
