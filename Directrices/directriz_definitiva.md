PROMPT PARA AGENTE DE GITHUB COPILOT: PROYECTO FINAL MLOPS
ROL: Experto en MLOps y desarrollo de software con enfoque en la calidad de código (SonarCloud).

OBJETIVO PRINCIPAL: Implementar un flujo de Machine Learning (ML) supervisado predictivo, adhiriéndose estrictamente a la arquitectura de carpetas predefinida, y asegurando que las funciones iniciales de procesamiento sean genéricas y reutilizables para cualquier dataset tabular, minimizando así el desperdicio de tokens en la ejecución.

RESTRICCIONES CLAVE:
* **CALIDAD DE CÓDIGO (SONARCLOUD):** Todo el código Python (.py) generado debe ser **código limpio**, mantenible y robusto. Debe adherirse a las mejores prácticas para pasar exitosamente las revisiones de calidad, seguridad y cobertura de SonarCloud. Evitar código duplicado, complejidad ciclomática alta y vulnerabilidades.
* **FLUJO SECUENCIAL:** Las tareas deben ejecutarse en orden. **La salida de un módulo (ej. `comprension_eda.ipynb`) es la entrada del siguiente (ej. `ft_engineering.py`)**. El flujo de datos debe ser coherente y estar documentado.

PRECONDICIONES (ASUMIDAS):
* El repositorio público en GitHub existe y contiene las tres ramas (developer, certification, master).
* [cite_start]La estructura de carpetas está creada (incluyendo mlops_pipeline/src/ y todos los archivos listados). [cite: 9]
* [cite_start]El entorno virtual está configurado y las dependencias (requirements.txt) están instaladas (vía setup.bat). [cite: 10, 11]
* El archivo de entrada Base_de_datos.csv se encuentra en la raíz del proyecto.

TAREAS DEL CICLO MLOPS (EJECUCIÓN SECUENCIAL EN LA RAMA developer):

1. Ingesta y Exploración de Datos (Enfoque Genérico)
* **Cargar_datos.ipynb:** Escribe el código necesario para cargar el `Base_de_datos.csv`.
* **comprension_eda.ipynb:** Desarrolla funciones genéricas y reutilizables para el EDA. El notebook debe incluir:
    * **Descripción General:** Presenta una descripción inicial del dataset. [cite: 13]
    * [cite_start]**Clasificación de Variables:** Identifica y clasifica correctamente los tipos de variables (categóricas, numéricas, ordinales, etc.). [cite: 14]
    * [cite_start]**Manejo de Nulos:** Revisa los valores nulos [cite: 15] [cite_start]y unifica su representación (ej. N/A, ?, - deben ser tratados como `np.nan`). [cite: 16]
    * [cite_start]**Limpieza Inicial:** Elimina variables irrelevantes (si aplica) [cite: 17][cite_start], convierte los datos a sus tipos correctos [cite: 18] [cite_start]y corrige inconsistencias. [cite: 19]
    * **Validación Post-Limpieza:** Ejecuta `describe()` *después* de ajustar los tipos de datos. [cite: 20]
    * **Análisis Univariable:**
        * Numéricas: Genera histogramas y boxplots. [cite: 21]
        * [cite_start]Categóricas: Usa `countplot`, `value_counts()` y tablas pivote. [cite: 22]
        * Estadísticas: Describe media, mediana, moda, rango, IQR, varianza, desviación estándar, skewness y kurtosis. [cite: 23]
        * [cite_start]Distribución: Identifica el tipo de distribución de las variables. [cite: 24]
    * **Análisis Bivariable/Multivariable:**
        * [cite_start]Analiza la relación entre las variables y la variable objetivo (a definir en el notebook). [cite: 25]
        * Incluye gráficos y tablas relevantes (ej. gráficos de dispersión, pairplots con `hue`, matrices de correlación). [cite: 26, 27, 28]
    * [cite_start]**Salida Crucial:** Define y documenta las reglas de validación de datos [cite: 29] [cite_start]e identifica posibles transformaciones y atributos derivados útiles para la siguiente etapa. [cite: 30]

2. Ingeniería de Características y Modelado (Implementación con Pipelines)
* **ft_engineering.py:** Implementa el proceso de ingeniería de características como un script.
    * Debe generar los features a partir del dataset base procesado en el EDA. [cite: 32]
    * [cite_start]Debe utilizar `sklearn.pipeline.Pipeline` y `ColumnTransformer` para aplicar transformaciones (escalado, codificación, imputación) de forma genérica. [cite: 34, 37]
    * [cite_start]Debe separar correctamente los conjuntos de entrenamiento y evaluación (X_train, X_test, etc.). [cite: 35]
    * Debe retornar un dataset limpio y listo para el modelado. [cite: 36]
    * [cite_start]Debe documentar claramente el flujo de transformación y las decisiones tomadas. [cite: 33, 38]
* **model_training_evaluation.py:** Escribe un script que:
    * [cite_start]Defina y utilice funciones reutilizables: `build_model()` (para estructurar el entrenamiento) [cite: 41] [cite_start]y `summarize_classification()` (para resumir métricas). [cite: 44]
    * [cite_start]Entrene múltiples modelos supervisados (ej. RandomForest, XGBoost, LogisticRegression). [cite: 40]
    * Aplique técnicas de validación (ej. cross-validation). [cite: 42]
    * [cite_start]Compare modelos usando métricas (accuracy, precision, recall, F1-score, ROC-AUC) [cite: 45] [cite_start]y gráficos (curvas ROC, matriz de confusión). [cite: 46]
    * Justifique y seleccione el mejor modelo basándose en performance, consistencia y escalabilidad. [cite: 47]
    * [cite_start]Guarde el objeto del modelo seleccionado (ej. .pkl o .joblib). [cite: 43]

3. Despliegue y Contenerización (Deployment)
* [cite_start]**model_deploy.py:** Desarrolla la API de despliegue (usando FastAPI o Flask). [cite: 55]
    * Carga el mejor modelo entrenado (ej. desde .pkl).
    * Define un endpoint `/predict` para recibir datos. [cite: 56]
    * [cite_start]Debe aceptar entrada en formato JSON y/o CSV. [cite: 57]
    * [cite_start]Debe soportar predicción por lotes (múltiples registros). [cite: 58]
    * Debe retornar la predicción en un formato estructurado (JSON, lista, etc.). [cite: 59]
* **Contenerización (Docker):**
    * Crea un `Dockerfile` funcional y un `.dockerignore`. [cite: 60]
    * La imagen debe contener el código, dependencias (requirements.txt) y el servidor de aplicación (ej. Uvicorn).

4. Monitoreo y Aplicación Web
* **model_monitoring.py:** Implementa el trabajo de monitoreo.
    * Define la periodicidad para el muestreo de datos.
    * [cite_start]Calcula métricas de Data Drift (ej. Kolmogorov-Smirnov, PSI, Chi-cuadrado). [cite: 49]
    * [cite_start]Genera alertas si se superan los umbrales críticos de desviación. [cite: 53]
* **Aplicación Streamlit:** Desarrolla una aplicación web funcional que: [cite: 50]
    * [cite_start]Visualice las métricas de drift (gráficos de comparación histórica vs. actual). [cite: 51]
    * [cite_start]Muestre indicadores visuales de alerta (ej. semáforo, barras de riesgo). [cite: 52]
    * Genere recomendaciones automáticas (ej. sugerencias de retraining).

5. Calidad y Documentación Final
* **README.md:** Genera el archivo documentando el caso de negocio, los principales hallazgos del EDA, y el proceso completo de ML/MLOps.
* **SonarCloud:**
    * [cite_start]Configura la integración de SonarCloud en el repositorio. [cite: 62]
    * [cite_start]Asegura que el repositorio esté vinculado y se generen y aprueben los resultados del análisis. [cite: 63]
    * Valida la calidad del código (complejidad, duplicación), seguridad (vulnerabilidades), cobertura de pruebas e integridad del estilo.

SALIDA ESPERADA: Implementación completa y documentada de todos los archivos y configuraciones solicitadas, con un enfoque en la reutilización de código y la **alta calidad (aprobada por SonarCloud)**.