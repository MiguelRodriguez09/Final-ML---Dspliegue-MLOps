PROMPT PARA AGENTE DE GITHUB COPILOT: PROYECTO FINAL MLOPS
ROL: Experto en MLOps y desarrollo de software con enfoque en la calidad de código (SonarCloud).
OBJETIVO PRINCIPAL: Implementar un flujo de Machine Learning (ML) supervisado predictivo, adhiriéndose estrictamente a la arquitectura de carpetas predefinida, y asegurando que las funciones iniciales de procesamiento sean genéricas y reutilizables para cualquier dataset tabular, minimizando así el desperdicio de tokens en la ejecución.
PRECONDICIONES (ASUMIDAS):

El repositorio público en GitHub existe y contiene las tres ramas (developer, certification, master).
La estructura de carpetas está creada (incluyendo mlops_pipeline/src/ y todos los archivos listados).
El entorno virtual está configurado y las dependencias (requirements.txt) están instaladas (vía setup.bat).
El archivo de entrada Base_de_datos.csv se encuentra en la raíz del proyecto.
TAREAS DEL CICLO MLOPS (EJECUCIÓN SECUENCIAL EN LA RAMA developer):

1. Ingesta y Exploración de Datos (Enfoque Genérico)
Cargar_datos.ipynb: Escribe el código necesario para cargar el Base_de_datos.csv.
comprension_eda.ipynb: Desarrolla funciones genéricas y reutilizables para el EDA, que funcionen con cualquier dataframe:
Exploración Inicial/Limpieza: Implementa la descripción, caracterización de datos (tipos), unificación de nulos (ej. N/A, ?, -) y corrección de tipos de datos (numéricos, categóricos, fechas).
Análisis Univariable: Utiliza describe(), histogramas, boxplots (numéricos) y countplot, value_counts() (categóricos).
Análisis Bivariable/Multivariable: Genera gráficos respecto a la variable objetivo (a definir en el notebook) y la matriz de correlación.
Salida Crucial: Define y documenta las reglas de validación de datos e identifica posibles transformaciones y atributos derivados útiles.

2. Ingeniería de Características y Modelado (Implementación con Pipelines)
ft_engineering.py: Implementa el proceso de ingeniería de características. Debe utilizar sklearn.pipeline.Pipeline y ColumnTransformer para transformar las características numéricas y categóricas de forma genérica (imputación, escalado, encoding). La salida deben ser los conjuntos de datos de entrenamiento y evaluación (X_train, X_test, etc.).
model_training_evaluation.py: Escribe un script que:
Defina y utilice las funciones reutilizables summarize_classification y build_model.
Entrene y evalúe diferentes modelos predictivos supervisados.
Seleccione el mejor modelo basándose en performance, consistency y scalability.
Genere la tabla resumen y gráficos comparativos de la evaluación.
Guarde el objeto del modelo seleccionado (ej. .pkl).

3. Despliegue y Contenerización (Deployment)
model_deploy.py: Desarrolla la API de despliegue.
Carga el mejor modelo entrenado (ej. desde .pkl o .joblib).
Define la lógica de predicción.
Utiliza FastAPI o Flask para exponer un endpoint /predict que soporte la predicción por lotes (batch).
Contenerización (Docker): Crea el Dockerfile y el .dockerignore necesario para construir una imagen que contenga el código, dependencias (requirements.txt) y el servidor de aplicación (ej. Uvicorn).

4. Monitoreo y Aplicación Web
model_monitoring.py: Implementa el trabajo de monitoreo.
Define la periodicidad para el muestreo de datos.
Calcula métricas de Data Drift, incluyendo Kolmogorov-Smirnov, PSI, Jensen-Shannon y Chi-cuadrado (para categóricas).
Genera alertas si se superan los umbrales críticos de desviación.
Aplicación Streamlit: Desarrolla la aplicación web que:
Visualiza las métricas de drift (gráficos de comparación histórica vs. actual, evolución temporal).
Muestra indicadores visuales de alerta (ej. semáforo, barras de riesgo).
Genera recomendaciones automáticas (ej. sugerencias de retraining o revisión).

5. Calidad y Documentación Final
README.md: Genera el archivo documentando el caso de negocio, los principales hallazgos del EDA, y el proceso completo de ML/MLOps.
SonarCloud: Configura la integración de SonarCloud en el repositorio para validar la calidad del código. Asegura la revisión de:
Calidad (Complejidad ciclomática, código duplicado, malas prácticas).
Seguridad (Exposición de datos sensibles, uso inseguro de librerías).
Cobertura de Pruebas (Líneas y funciones validadas).
Integridad y Estilo (Convenciones de nombramiento, indentación, consistencia).

SALIDA ESPERADA: Implementación completa y documentada de todos los archivos y configuraciones solicitadas, con un enfoque en la reutilización de código en las etapas iniciales.