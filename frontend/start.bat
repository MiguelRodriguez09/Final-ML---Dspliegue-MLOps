@echo off
REM ============================================
REM Quick Start - Frontend Solo
REM ============================================

echo.
echo ============================================
echo    Iniciando Frontend MLOps
echo ============================================
echo.

REM Check current directory
if exist "frontend\server.py" (
    echo [OK] Directorio correcto
    cd frontend
) else if exist "server.py" (
    echo [OK] Ya en directorio frontend
) else (
    echo [ERROR] No se encuentra el directorio frontend
    echo Por favor ejecuta este script desde la raiz del proyecto
    pause
    exit /b 1
)

echo [INFO] Iniciando servidor en http://localhost:8080
echo [INFO] API esperada en http://localhost:5000
echo.

python server.py

pause
