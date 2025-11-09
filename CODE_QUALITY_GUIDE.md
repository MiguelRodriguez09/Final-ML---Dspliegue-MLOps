# 📐 Guía de Calidad de Código - MLOps Project

## 🎯 Estándares de Código

Este proyecto sigue estándares estrictos de calidad de código para garantizar mantenibilidad, legibilidad y robustez.

---

## 🔍 Herramientas de Análisis

### SonarCloud
- **Análisis automático** en cada push/PR
- **Quality Gate** configurado para mantener calidad mínima
- **Métricas monitoreadas**: Bugs, Vulnerabilidades, Code Smells, Duplicación, Cobertura

### Pylint
- Configurado en `.pylintrc`
- Ejecutar localmente: `pylint mlops_pipeline/src/*.py`
- Score objetivo: ≥ 8.0/10

---

## ✅ Reglas Aplicadas

### 1. Complejidad Cognitiva

**Máximo**: 15 por función

**Razón**: Funciones complejas son difíciles de entender, mantener y probar.

**Solución**:
- Extraer subfunciones
- Usar early returns
- Aplicar principio de responsabilidad única

```python
# ❌ MAL - Complejidad alta
def procesar_datos(df):
    if df is not None:
        if len(df) > 0:
            for col in df.columns:
                if df[col].dtype == 'object':
                    if df[col].nunique() < 10:
                        # ... código complejo
                        pass

# ✅ BIEN - Dividido en funciones
def procesar_datos(df):
    validar_dataframe(df)
    columnas_categoricas = obtener_columnas_categoricas(df)
    return transformar_categoricas(df, columnas_categoricas)
```

### 2. Duplicación de Código

**Máximo**: 3% de líneas duplicadas

**Razón**: DRY (Don't Repeat Yourself) mejora mantenibilidad.

**Solución**:
- Crear funciones reutilizables en `utils.py`
- Usar herencia y composición
- Centralizar constantes en `config.py`

```python
# ❌ MAL - Código duplicado
def guardar_modelo_rf(modelo):
    with open('rf_model.pkl', 'wb') as f:
        pickle.dump(modelo, f)

def guardar_modelo_xgb(modelo):
    with open('xgb_model.pkl', 'wb') as f:
        pickle.dump(modelo, f)

# ✅ BIEN - Función genérica
def guardar_modelo(modelo, nombre):
    ruta = MODELS_DIR / f'{nombre}.pkl'
    guardar_pickle(modelo, ruta)
```

### 3. Funciones Largas

**Máximo**: 50 líneas por función

**Razón**: Funciones cortas son más fáciles de entender y probar.

**Solución**:
- Dividir en subfunciones
- Extraer lógica a métodos privados
- Un nivel de abstracción por función

### 4. Manejo de Excepciones

**Regla**: Capturar excepciones específicas, no `Exception`

```python
# ❌ MAL - Excepción genérica
try:
    df = pd.read_csv(archivo)
except Exception as e:
    print(f"Error: {e}")

# ✅ BIEN - Excepciones específicas
try:
    df = pd.read_csv(archivo)
except FileNotFoundError:
    logger.error(f"Archivo no encontrado: {archivo}")
    raise
except pd.errors.ParserError:
    logger.error(f"Error al parsear CSV: {archivo}")
    raise
```

### 5. Documentación

**Regla**: Todas las funciones públicas deben tener docstrings

```python
# ✅ BIEN - Docstring completo
def entrenar_modelo(X_train, y_train, modelo):
    """
    Entrena un modelo de ML con los datos proporcionados.
    
    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
        modelo: Instancia del modelo a entrenar
        
    Returns:
        Modelo entrenado
        
    Raises:
        ValueError: Si los datos están vacíos
    """
    if len(X_train) == 0:
        raise ValueError("Datos de entrenamiento vacíos")
    
    return modelo.fit(X_train, y_train)
```

### 6. Type Hints

**Regla**: Usar type hints en funciones públicas

```python
from typing import List, Dict, Tuple

def procesar_features(
    df: pd.DataFrame,
    columnas: List[str]
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Procesa features del DataFrame."""
    # ... implementación
    return df_procesado, metadata
```

### 7. Constantes

**Regla**: Definir constantes en UPPER_CASE en `config.py`

```python
# ❌ MAL - Magic numbers
if accuracy > 0.85:
    print("Modelo aprobado")

# ✅ BIEN - Constante definida
ACCURACY_THRESHOLD = 0.85

if accuracy > ACCURACY_THRESHOLD:
    logger.info("Modelo aprobado")
```

### 8. Imports

**Regla**: Organizar imports según PEP 8

```python
# 1. Standard library
import json
import pickle
from pathlib import Path
from typing import Dict, List

# 2. Third party
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 3. Local imports
from .config import MODELS_DIR, RANDOM_STATE
from .utils import guardar_pickle, cargar_json
```

---

## 🛠️ Herramientas Recomendadas

### Formateo Automático

```bash
# Black - Formateo de código
pip install black
black mlops_pipeline/src/

# isort - Ordenar imports
pip install isort
isort mlops_pipeline/src/
```

### Análisis Estático

```bash
# Pylint
pylint mlops_pipeline/src/*.py

# Flake8
pip install flake8
flake8 mlops_pipeline/src/

# mypy - Type checking
pip install mypy
mypy mlops_pipeline/src/
```

---

## 📊 Métricas de Calidad

### Objetivos del Proyecto

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| **Bugs** | 0 | - |
| **Vulnerabilities** | 0 | - |
| **Code Smells** | < 50 | - |
| **Coverage** | ≥ 80% | - |
| **Duplicación** | < 3% | - |
| **Maintainability** | A | - |
| **Reliability** | A | - |
| **Security** | A | - |

---

## 🔄 Flujo de Trabajo

### Antes de Commit

1. **Formatear código**:
   ```bash
   black mlops_pipeline/src/
   isort mlops_pipeline/src/
   ```

2. **Ejecutar linter**:
   ```bash
   pylint mlops_pipeline/src/*.py
   ```

3. **Verificar tests**:
   ```bash
   pytest tests/
   ```

### Después de Push

1. **Revisar SonarCloud**: [Ver Dashboard](https://sonarcloud.io/project/overview?id=MiguelRodriguez09_Final-ML---Dspliegue-MLOps)
2. **Corregir issues críticos** antes de merge
3. **Verificar Quality Gate** pasa

---

## 📝 Checklist de Code Review

- [ ] ¿El código sigue PEP 8?
- [ ] ¿Todas las funciones tienen docstrings?
- [ ] ¿Se usan type hints?
- [ ] ¿No hay código duplicado?
- [ ] ¿Las funciones son cortas (< 50 líneas)?
- [ ] ¿La complejidad es baja (< 15)?
- [ ] ¿Se manejan excepciones específicas?
- [ ] ¿Se usan constantes en lugar de magic numbers?
- [ ] ¿Los nombres son descriptivos?
- [ ] ¿Hay tests para código crítico?

---

## 🚨 Issues Comunes y Soluciones

### Issue: "Cognitive Complexity of this function is too high"

**Solución**: Extraer subfunciones

```python
# Antes
def analizar_drift(df1, df2):
    # 100 líneas de código complejo
    pass

# Después
def analizar_drift(df1, df2):
    metricas_numericas = calcular_drift_numerico(df1, df2)
    metricas_categoricas = calcular_drift_categorico(df1, df2)
    return consolidar_metricas(metricas_numericas, metricas_categoricas)
```

### Issue: "Object of type int64 is not JSON serializable"

**Solución**: Usar función de conversión

```python
from utils import convert_numpy_to_python, guardar_json

# Antes
with open('data.json', 'w') as f:
    json.dump(data, f)  # ❌ Error con numpy types

# Después
guardar_json(data, 'data.json')  # ✅ Maneja numpy types
```

### Issue: "Refactor this function to reduce its Cognitive Complexity"

**Solución**: Usar early returns y guard clauses

```python
# Antes
def procesar(data):
    if data is not None:
        if len(data) > 0:
            if validar(data):
                return transformar(data)
    return None

# Después
def procesar(data):
    if data is None or len(data) == 0:
        return None
    
    if not validar(data):
        return None
    
    return transformar(data)
```

---

## 📚 Referencias

- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [SonarCloud Python Rules](https://rules.sonarsource.com/python)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Clean Code in Python](https://github.com/zedr/clean-code-python)

---

**¡Mantener código limpio es responsabilidad de todos!** 🎯
