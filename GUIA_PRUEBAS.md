# 🧪 GUÍA DE PRUEBAS POST-REFACTORIZACIÓN

## ✅ ESTADO ACTUAL
- ✅ 7 archivos actualizados con nuevas rutas
- ✅ 30+ rutas modificadas correctamente
- ✅ 0 cambios en lógica de negocio
- ✅ Carpeta `reports/plots/` existe
- ⚠️ Warnings de estilo (SonarQube) - no afectan funcionalidad

---

## 🚀 PASO 1: PRUEBAS LOCALES (SIN DOCKER)

### 1.1 Probar API Flask

```powershell
# Desde la raíz del proyecto
python mlops_pipeline\src\model_deploy.py
```

**Resultado esperado:**
```
INFO - Modelo cargado desde: C:\Users\Asus\Desktop\Proyecto\models\best_model.pkl
INFO - Preprocessor cargado desde: C:\Users\Asus\Desktop\Proyecto\models\preprocessor.pkl
INFO - Metadatos del modelo cargados
INFO - Nombres de features cargados: X features
 * Running on http://127.0.0.1:5000
```

**Probar endpoint:**
```powershell
# En otra terminal
curl http://localhost:5000/
curl http://localhost:5000/model-info
```

---

### 1.2 Probar Dashboard Streamlit

```powershell
# Desde la raíz del proyecto
streamlit run mlops_pipeline\src\streamlit_app.py
```

**Resultado esperado:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Verificar en navegador:**
- Abre http://localhost:8501
- Verifica que carga sin errores
- Revisa que muestra métricas y gráficos

---

### 1.3 Probar Frontend

```powershell
# Desde la carpeta frontend
cd frontend
python server.py
```

**Resultado esperado:**
```
Server running at: http://localhost:8080
Serving directory: C:\Users\Asus\Desktop\Proyecto\frontend
```

**Verificar en navegador:**
- Abre http://localhost:8080
- Verifica que la interfaz carga
- Intenta hacer una predicción (requiere API corriendo)

---

## 🐳 PASO 2: PRUEBAS CON DOCKER

### 2.1 Construir imágenes Docker

```powershell
# Opción 1: Usar Makefile
make build

# Opción 2: Comando directo
docker-compose -f docker\docker-compose.yml build --no-cache
```

**Resultado esperado:**
```
[+] Building...
 => [api internal] load .dockerignore
 => [dashboard internal] load .dockerignore
 => [frontend internal] load .dockerignore
Successfully built
```

---

### 2.2 Iniciar servicios

```powershell
# Opción 1: Usar Makefile
make up

# Opción 2: Comando directo
docker-compose -f docker\docker-compose.yml up -d
```

**Resultado esperado:**
```
[+] Running 4/4
 ✔ Network mlops-network       Created
 ✔ Container mlops-api          Started
 ✔ Container mlops-dashboard    Started
 ✔ Container mlops-frontend     Started
```

---

### 2.3 Verificar estado de contenedores

```powershell
# Ver contenedores corriendo
docker ps

# Ver logs
docker-compose -f docker\docker-compose.yml logs -f
```

**Contenedores esperados:**
- `mlops-api` (puerto 5000)
- `mlops-dashboard` (puerto 8501)
- `mlops-frontend` (puerto 8080)

---

### 2.4 Probar servicios Docker

**API:**
```powershell
curl http://localhost:5000/
curl http://localhost:5000/model-info
```

**Dashboard:**
- Navega a http://localhost:8501
- Verifica que carga correctamente

**Frontend:**
- Navega a http://localhost:8080
- Prueba hacer una predicción

---

## 🔍 PASO 3: VERIFICACIÓN DE ARCHIVOS

### 3.1 Verificar que los archivos existen

```powershell
# Modelos
Test-Path "models\best_model.pkl"
Test-Path "models\preprocessor.pkl"
Test-Path "models\model_metadata.json"

# Datos procesados
Test-Path "data\processed\train_data.csv"
Test-Path "data\processed\test_data.csv"
Test-Path "data\processed\data_cleaned.csv"

# Datos raw
Test-Path "data\raw\Churn_Modelling.csv"

# Metadatos
Test-Path "data\metadata\eda_metadata.json"
Test-Path "data\metadata\feature_engineering_metadata.json"
Test-Path "data\metadata\drift_report.json"
```

**Resultado esperado:** Todos deben devolver `True`

---

### 3.2 Verificar estructura de carpetas

```powershell
tree /F /A | Select-Object -First 100
```

**Verificar que existen:**
- `data/raw/`
- `data/processed/`
- `data/metadata/`
- `models/`
- `reports/plots/`
- `docker/`
- `mlops_pipeline/src/`
- `frontend/static/`

---

## 🧪 PASO 4: PRUEBAS FUNCIONALES

### 4.1 Test de Feature Engineering

```powershell
# Ejecutar script de feature engineering
python mlops_pipeline\src\ft_engineering.py
```

**Verificar que genera:**
- `models/preprocessor.pkl`
- `data/processed/train_data.csv`
- `data/processed/test_data.csv`
- `data/metadata/feature_engineering_metadata.json`

---

### 4.2 Test de Training

```powershell
# Ejecutar script de entrenamiento
python mlops_pipeline\src\model_training_evaluation.py
```

**Verificar que genera:**
- `models/best_model.pkl`
- `models/model_metadata.json`
- `reports/plots/model_comparison.png`
- `reports/plots/confusion_matrices.png`
- `reports/plots/roc_curves.png`

---

### 4.3 Test de Monitoring

```powershell
# Ejecutar script de monitoreo
python mlops_pipeline\src\model_monitoring.py
```

**Verificar que genera:**
- `data/metadata/drift_report.json`
- `reports/plots/drift_summary.png`

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: "FileNotFoundError: No such file or directory"

**Causa:** Archivo no está en la ubicación esperada

**Solución:**
1. Verifica que el archivo existe: `Test-Path "ruta\al\archivo"`
2. Si no existe, ejecútalo desde el script que lo genera
3. Revisa que la ruta en el código es correcta

---

### Error: "ModuleNotFoundError: No module named 'mlops_pipeline'"

**Causa:** Python no encuentra el módulo

**Solución:**
```powershell
# Agregar al PYTHONPATH
$env:PYTHONPATH = "C:\Users\Asus\Desktop\Proyecto"
python mlops_pipeline\src\nombre_script.py
```

---

### Error: Docker build falla

**Causa:** Context o Dockerfile incorrectos

**Solución:**
1. Verifica que estás en la raíz del proyecto
2. Revisa los Dockerfiles en `docker/`
3. Asegúrate que los COPY apuntan a las rutas correctas

**Ejemplo de línea correcta en Dockerfile:**
```dockerfile
COPY models/best_model.pkl /app/models/best_model.pkl
COPY data/metadata/ /app/data/metadata/
```

---

### Error: API no encuentra el modelo

**Causa:** Rutas incorrectas en model_deploy.py

**Solución:**
- Ya está corregido en la refactorización
- Si persiste, verifica manualmente las líneas 45-65 de `model_deploy.py`

---

### Error: Dashboard no muestra datos

**Causa:** drift_report.json o model_metadata.json no existen

**Solución:**
1. Ejecuta primero el script de monitoreo:
   ```powershell
   python mlops_pipeline\src\model_monitoring.py
   ```
2. Verifica que se generó el archivo:
   ```powershell
   Test-Path "data\metadata\drift_report.json"
   ```

---

## 📊 CHECKLIST FINAL

### Pruebas Locales
- [ ] API Flask inicia sin errores
- [ ] API responde en http://localhost:5000
- [ ] Dashboard Streamlit inicia sin errores
- [ ] Dashboard carga en http://localhost:8501
- [ ] Frontend inicia sin errores
- [ ] Frontend carga en http://localhost:8080

### Pruebas Docker
- [ ] Docker build completa sin errores
- [ ] Los 3 contenedores inician correctamente
- [ ] API responde desde Docker
- [ ] Dashboard carga desde Docker
- [ ] Frontend carga desde Docker

### Verificación de Archivos
- [ ] Todos los archivos .pkl existen en `models/`
- [ ] Todos los archivos .csv existen en `data/processed/`
- [ ] Todos los metadatos existen en `data/metadata/`
- [ ] Carpeta `reports/plots/` existe

### Pruebas Funcionales
- [ ] Feature Engineering ejecuta correctamente
- [ ] Model Training ejecuta correctamente
- [ ] Model Monitoring ejecuta correctamente
- [ ] Se generan todos los gráficos en `reports/plots/`
- [ ] Predicción individual funciona
- [ ] Predicción por lote funciona

---

## 🎯 RESULTADO ESPERADO

Si todas las pruebas pasan:

✅ **Tu proyecto está completamente refactorizado y funcional**

Con la nueva estructura:
```
Proyecto/
├── data/
│   ├── raw/ ✅ Datos originales
│   ├── processed/ ✅ Datos procesados
│   └── metadata/ ✅ Metadatos y reportes
├── models/ ✅ Modelos entrenados
├── reports/plots/ ✅ Gráficos generados
├── mlops_pipeline/src/ ✅ Código Python
├── docker/ ✅ Archivos Docker
├── frontend/ ✅ Interfaz web
└── scripts/ ✅ Scripts de automatización
```

---

## 📞 SOPORTE

Si encuentras algún error:
1. Revisa los logs de los servicios
2. Verifica que todas las rutas están actualizadas
3. Consulta el archivo `REFACTORIZACION_COMPLETADA.md`
4. Revisa el análisis original en `ANALISIS_REFACTORIZACION.md`

---

**Última actualización:** 10/11/2025  
**Estado:** ✅ Listo para pruebas  
**Confianza:** Alta (todas las rutas actualizadas)
