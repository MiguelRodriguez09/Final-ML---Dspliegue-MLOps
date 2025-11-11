@echo off
REM ============================================
REM  Script de Ejecución del Pipeline MLOps
REM ============================================
REM  Este script ejecuta el pipeline completo de MLOps
REM  en el orden correcto.
REM ============================================

echo.
echo ====================================================
echo         PIPELINE MLOPS - EJECUCION COMPLETA
echo ====================================================
echo.

REM Verificar que el entorno virtual existe
if not exist "..\Proyecto-venv\Scripts\Activate.bat" (
    echo [ERROR] Entorno virtual no encontrado.
    echo Por favor, ejecute set_up.bat primero.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [1/6] Activando entorno virtual...
call ..\Proyecto-venv\Scripts\activate.bat
echo.

REM Cambiar al directorio raíz del proyecto
cd ..

REM Feature Engineering
echo [2/6] Ejecutando Feature Engineering...
python mlops_pipeline\src\ft_engineering.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Feature Engineering fallo.
    pause
    exit /b 1
)
echo.

REM Entrenamiento de Modelos
echo [3/6] Entrenando modelos...
python mlops_pipeline\src\model_training_evaluation.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Entrenamiento de modelos fallo.
    pause
    exit /b 1
)
echo.

REM Monitoreo de Drift
echo [4/6] Ejecutando monitoreo de drift...
python mlops_pipeline\src\model_monitoring.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Monitoreo de drift fallo.
    pause
    exit /b 1
)
echo.

REM Informar sobre los pasos manuales
echo [5/6] PASOS MANUALES REQUERIDOS:
echo.
echo    Para ejecutar los notebooks de EDA:
echo    1. jupyter notebook mlops_pipeline/src/cargar_datos.ipynb
echo    2. jupyter notebook mlops_pipeline/src/compresion_eda.ipynb
echo.

echo [6/6] Para iniciar los servicios:
echo.
echo    API de Prediccion:
echo       python mlops_pipeline/src/model_deploy.py
echo.
echo    Dashboard de Monitoreo:
echo       streamlit run mlops_pipeline/src/streamlit_app.py
echo.

echo ====================================================
echo         PIPELINE EJECUTADO EXITOSAMENTE
echo ====================================================
echo.
echo Archivos generados:
echo   DATOS:
echo   - data/processed/data_cleaned.csv
echo   - data/processed/train_data.csv
echo   - data/processed/test_data.csv
echo.
echo   MODELOS:
echo   - models/preprocessor.pkl
echo   - models/best_model.pkl
echo   - models/model_metadata.json
echo.
echo   METADATOS:
echo   - data/metadata/eda_metadata.json
echo   - data/metadata/feature_engineering_metadata.json
echo   - data/metadata/drift_report.json
echo.
echo   GRAFICOS:
echo   - reports/plots/model_comparison.png
echo   - reports/plots/confusion_matrices.png
echo   - reports/plots/roc_curves.png
echo   - reports/plots/drift_summary.png
echo.
echo ====================================================
echo.

pause
