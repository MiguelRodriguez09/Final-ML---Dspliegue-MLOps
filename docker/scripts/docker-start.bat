@echo off
REM ============================================
REM MLOps Pipeline - Docker Start Script (Windows)
REM ============================================
REM Script para iniciar los servicios Docker en Windows
REM Uso: docker-start.bat [api|dashboard|all]
REM ============================================

setlocal enabledelayedexpansion

echo ============================================
echo    MLOps Pipeline - Docker Deployment
echo ============================================
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado. Por favor, instala Docker Desktop primero.
    exit /b 1
)

REM Verificar si Docker Compose está instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose no esta instalado.
    exit /b 1
)

REM Verificar que los artefactos existen
echo [INFO] Verificando artefactos del modelo...
if not exist "best_model.pkl" (
    echo [WARNING] best_model.pkl no encontrado.
    echo [INFO] Ejecuta el pipeline de entrenamiento primero:
    echo [INFO]   python mlops_pipeline\src\model_training_evaluation.py
)

REM Determinar qué servicio iniciar
set SERVICE=%1
if "%SERVICE%"=="" set SERVICE=all

if "%SERVICE%"=="api" (
    echo [INFO] Construyendo imagen de la API...
    docker build -t mlops-api:latest -f Dockerfile .
    if errorlevel 1 (
        echo [ERROR] Error al construir la imagen de la API
        exit /b 1
    )
    echo [SUCCESS] Imagen de API construida
    
    echo [INFO] Iniciando servicio de API...
    docker run -d --name mlops-api -p 5000:5000 ^
        -v "%cd%\best_model.pkl:/app/best_model.pkl:ro" ^
        -v "%cd%\preprocessor.pkl:/app/preprocessor.pkl:ro" ^
        -v "%cd%\model_metadata.json:/app/model_metadata.json:ro" ^
        -v "%cd%\feature_engineering_metadata.json:/app/feature_engineering_metadata.json:ro" ^
        mlops-api:latest
    
    echo [SUCCESS] API iniciada en http://localhost:5000
    
) else if "%SERVICE%"=="dashboard" (
    echo [INFO] Construyendo imagen del Dashboard...
    docker build -t mlops-dashboard:latest -f Dockerfile.streamlit .
    if errorlevel 1 (
        echo [ERROR] Error al construir la imagen del Dashboard
        exit /b 1
    )
    echo [SUCCESS] Imagen de Dashboard construida
    
    echo [INFO] Iniciando servicio de Dashboard...
    docker run -d --name mlops-dashboard -p 8501:8501 ^
        -v "%cd%\train_data.csv:/app/train_data.csv:ro" ^
        -v "%cd%\test_data.csv:/app/test_data.csv:ro" ^
        -v "%cd%\drift_report.json:/app/drift_report.json:ro" ^
        -v "%cd%\model_metadata.json:/app/model_metadata.json:ro" ^
        mlops-dashboard:latest
    
    echo [SUCCESS] Dashboard iniciado en http://localhost:8501
    
) else if "%SERVICE%"=="all" (
    echo [INFO] Construyendo todas las imagenes...
    docker-compose build
    if errorlevel 1 (
        echo [ERROR] Error al construir las imagenes
        exit /b 1
    )
    echo [SUCCESS] Imagenes construidas
    
    echo [INFO] Iniciando todos los servicios...
    docker-compose up -d
    if errorlevel 1 (
        echo [ERROR] Error al iniciar los servicios
        exit /b 1
    )
    echo [SUCCESS] Servicios iniciados
    
    echo.
    echo [SUCCESS] Deployment completado!
    echo.
    echo Servicios disponibles:
    echo   - API:       http://localhost:5000
    echo   - Dashboard: http://localhost:8501
    echo.
    echo Comandos utiles:
    echo   - Ver logs:        docker-compose logs -f
    echo   - Detener:         docker-compose down
    echo   - Ver estado:      docker-compose ps
    echo.
    
) else (
    echo [ERROR] Servicio desconocido: %SERVICE%
    echo Uso: docker-start.bat [api^|dashboard^|all]
    exit /b 1
)

REM Esperar a que los servicios estén listos
echo [INFO] Esperando a que los servicios esten listos...
timeout /t 5 /nobreak >nul

echo [SUCCESS] Deployment completado! 
echo.
echo Para verificar el estado de los contenedores:
echo   docker ps
echo.
echo Para ver los logs:
echo   docker-compose logs -f

endlocal
