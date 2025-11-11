# Módulo: Análisis Exploratorio de Datos (EDA)

## 1. Propósito

Este módulo se encarga del **análisis exploratorio de datos (EDA)** para el dataset de churn bancario. Incluye:
- Carga y exploración inicial de datos
- Análisis de calidad de datos (valores nulos, duplicados, tipos de datos)
- Análisis estadístico descriptivo
- Detección de outliers
- Análisis de distribuciones
- Análisis de correlaciones
- Visualizaciones exploratorias
- Generación del dataset limpio (`data_cleaned.csv`)

---

## 2. Instrucciones de Ejecución

### 2.1. Prerrequisitos
```powershell
# Asegurarse de que el entorno virtual esté activado
.\Proyecto-venv\Scripts\Activate.ps1

# Verificar que el dataset original exista
# Debe estar en: data/raw/Churn_Modelling.csv
```

### 2.2. Ejecución del Notebook

**Opción 1: Jupyter Notebook (Recomendado)**
```powershell
# Iniciar Jupyter Notebook
jupyter notebook

# Navegar a: mlops_pipeline/src/compresion_eda.ipynb
# Ejecutar todas las celdas: Cell > Run All
```

**Opción 2: Jupyter Lab**
```powershell
# Iniciar Jupyter Lab
jupyter lab

# Abrir: mlops_pipeline/src/compresion_eda.ipynb
# Ejecutar todas las celdas
```

**Opción 3: VS Code**
```powershell
# Abrir el notebook en VS Code
code mlops_pipeline/src/compresion_eda.ipynb

# Ejecutar todas las celdas usando el botón "Run All"
```

### 2.3. Salidas Esperadas

Después de ejecutar el notebook, se generarán:
- **Archivo:** `data/processed/data_cleaned.csv` - Dataset limpio
- **Archivo:** `data/metadata/eda_metadata.json` - Metadatos del EDA
- **Visualizaciones:** Gráficos en el notebook (distribuciones, boxplots, correlaciones)

---

## 3. Mapeo de Requisitos del Checklist

| Requisito del Checklist | Ubicación en el Código | Descripción |
|:---|:---|:---|
| **¿Se realiza un EDA completo?** | Todo el notebook `compresion_eda.ipynb` | Análisis exhaustivo de todas las variables |
| **¿Se cargan los datos correctamente?** | Celda inicial con `pd.read_csv()` | Carga desde `data/raw/Churn_Modelling.csv` |
| **¿Se analizan los tipos de datos?** | Sección "Tipos de datos" con `df.dtypes` | Verificación de tipos de cada columna |
| **¿Se identifican valores nulos?** | Sección "Valores nulos" con `df.isnull().sum()` | Detección y cuantificación de nulos |
| **¿Se detectan duplicados?** | Sección "Duplicados" con `df.duplicated().sum()` | Identificación de registros duplicados |
| **¿Se realiza análisis estadístico?** | Sección con `df.describe()` | Estadísticas descriptivas (mean, std, min, max, quartiles) |
| **¿Se detectan outliers?** | Sección "Outliers" con boxplots | Visualización con `sns.boxplot()` |
| **¿Se analizan distribuciones?** | Sección "Distribuciones" con histogramas | Gráficos con `plt.hist()` y `sns.histplot()` |
| **¿Se analiza la variable objetivo?** | Sección "Target Variable" | Análisis de balance de clases (Exited) |
| **¿Se analizan correlaciones?** | Sección "Correlaciones" con heatmap | Matriz de correlación con `sns.heatmap()` |
| **¿Se visualizan variables categóricas?** | Sección con `countplot` | Gráficos de barras para Geography, Gender |
| **¿Se visualizan variables numéricas?** | Sección con histogramas y density plots | Distribuciones de Age, CreditScore, Balance |
| **¿Se generan insights del negocio?** | Secciones de análisis y conclusiones | Interpretación de patrones de churn |
| **¿Se limpia el dataset?** | Secciones de limpieza de datos | Eliminación de columnas innecesarias, tratamiento de nulos |
| **¿Se genera data_cleaned.csv?** | Última celda con `df.to_csv()` | Exportación a `data/processed/data_cleaned.csv` |
| **¿Se guardan metadatos?** | Celda final con `json.dump()` | Exportación a `data/metadata/eda_metadata.json` |

---

## 4. Estructura del Notebook

### 4.1. Secciones Principales

1. **Importación de Librerías**
   - pandas, numpy, matplotlib, seaborn

2. **Carga de Datos**
   - Lectura del CSV original
   - Vista preliminar del dataset

3. **Análisis de Calidad**
   - Verificación de tipos de datos
   - Detección de valores nulos
   - Detección de duplicados
   - Identificación de outliers

4. **Análisis Estadístico**
   - Estadísticas descriptivas
   - Análisis univariado
   - Análisis bivariado

5. **Visualizaciones**
   - Distribuciones de variables numéricas
   - Análisis de variables categóricas
   - Matriz de correlación
   - Boxplots para outliers

6. **Análisis del Target**
   - Balance de clases
   - Relación con otras variables

7. **Limpieza de Datos**
   - Eliminación de columnas innecesarias
   - Tratamiento de outliers (si es necesario)
   - Corrección de tipos de datos

8. **Exportación**
   - Guardado de data_cleaned.csv
   - Guardado de metadatos

---

## 5. Insights Clave del EDA

### 5.1. Características del Dataset
- **Total de registros:** 10,000 clientes
- **Total de variables:** 14 columnas
- **Variable objetivo:** `Exited` (0 = No churn, 1 = Churn)
- **Balance de clases:** Aprox. 20% churn, 80% no churn (desbalanceado)

### 5.2. Variables Numéricas
- **CreditScore:** Rango 350-850
- **Age:** Rango 18-92, posibles outliers en edades altas
- **Tenure:** 0-10 años de antigüedad
- **Balance:** Saldo de cuenta, muchos ceros
- **EstimatedSalary:** Salario estimado, distribución uniforme

### 5.3. Variables Categóricas
- **Geography:** France, Germany, Spain
- **Gender:** Male, Female
- **HasCrCard:** 0 o 1 (mayoría tiene tarjeta)
- **IsActiveMember:** 0 o 1 (50/50 aproximadamente)

### 5.4. Correlaciones Importantes
- **Age** tiene correlación positiva con Churn
- **NumOfProducts** y **IsActiveMember** tienen correlación negativa con Churn
- **Geography** (Germany) tiene mayor tasa de churn

### 5.5. Hallazgos de Negocio
- Clientes de mayor edad tienden a hacer más churn
- Clientes con balance cero tienen comportamiento diferente
- Clientes inactivos tienen mayor probabilidad de churn
- Geografía es un factor importante (Germany tiene más churn)

---

## 6. Archivos Generados

| Archivo | Ubicación | Contenido |
|:---|:---|:---|
| **data_cleaned.csv** | `data/processed/` | Dataset limpio, listo para feature engineering |
| **eda_metadata.json** | `data/metadata/` | Metadatos del análisis (columnas, tipos, estadísticas) |

---

## 7. Próximos Pasos

Después de completar el EDA, continuar con:
1. **Feature Engineering** → `ft_engineering.py`
2. Transformación de variables
3. Split train/test
4. Entrenamiento de modelos

---

## 8. Troubleshooting

### Problema: "FileNotFoundError: data/raw/Churn_Modelling.csv"
**Solución:** Verificar que el archivo exista en la ubicación correcta.

### Problema: "ModuleNotFoundError: No module named 'seaborn'"
**Solución:** Instalar dependencias: `pip install -r requirements.txt`

### Problema: "Memory Error al cargar el dataset"
**Solución:** El dataset es pequeño (10K registros), verificar memoria disponible.

---

## 9. Notas Adicionales

- El notebook está diseñado para ser ejecutado de forma secuencial
- Algunas visualizaciones pueden tardar en renderizarse
- Se recomienda tener al menos 4GB de RAM disponible
- Tiempo estimado de ejecución: 2-5 minutos

---

**Contacto:**  
Para preguntas sobre este módulo, referirse al README principal del proyecto.
