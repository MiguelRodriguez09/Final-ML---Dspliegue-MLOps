@echo off
REM ============================================
REM MLOps Pipeline - Quick Start (Windows)
REM ============================================
REM Script para inicio rápido del proyecto
REM ============================================

echo.
echo ============================================
echo    MLOps Pipeline - Quick Start
echo ============================================
echo.

echo [1/5] Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado!
    echo Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [OK] Docker instalado

REM Cambiar al directorio raíz del proyecto
cd /d "%~dp0.."

echo.
echo [2/5] Verificando artefactos del modelo...
if not exist "models\best_model.pkl" (
    echo [WARNING] best_model.pkl no encontrado en models\
    echo [INFO] Generando artefactos del modelo...
    python mlops_pipeline\src\model_training_evaluation.py
    if errorlevel 1 (
        echo [ERROR] Error al generar artefactos
        pause
        exit /b 1
    )
)
echo [OK] Artefactos disponibles

echo.
echo [3/5] Construyendo imagenes Docker...
docker-compose -f docker\docker-compose.yml build
if errorlevel 1 (
    echo [ERROR] Error al construir imagenes
    pause
    exit /b 1
)
echo [OK] Imagenes construidas

echo.
echo [4/5] Iniciando servicios...
docker-compose -f docker\docker-compose.yml up -d
if errorlevel 1 (
    echo [ERROR] Error al iniciar servicios
    pause
    exit /b 1
)
echo [OK] Servicios iniciados

echo.
echo [5/5] Verificando servicios...
timeout /t 10 /nobreak >nul
docker-compose -f docker\docker-compose.yml ps

echo.
echo ============================================
echo    Deployment Completado!
echo ============================================
echo.
echo Servicios disponibles:
echo   - API:       http://localhost:5000
echo   - Dashboard: http://localhost:8501
echo.
echo Comandos utiles:
echo   - Ver logs:        docker-compose -f docker\docker-compose.yml logs -f
echo   - Detener:         docker-compose -f docker\docker-compose.yml down
echo   - Estado:          docker-compose -f docker\docker-compose.yml ps
echo   - Reiniciar:       docker-compose -f docker\docker-compose.yml restart
echo   - O usa Make:      make up / make down / make logs
echo.
echo Para mas informacion, consulta:
echo   - DOCKER_README.md (inicio rapido)
echo   - DOCKER_GUIDE.md  (guia completa)
echo.

choice /C YN /M "Deseas abrir los servicios en el navegador"
if errorlevel 2 goto :end
if errorlevel 1 (
    start http://localhost:5000
    start http://localhost:8501
)

:end
echo.
echo Presiona cualquier tecla para salir...
pause >nul
