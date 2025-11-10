@echo off
REM ============================================
REM MLOps Frontend Launcher
REM ============================================

echo ============================================
echo     MLOps Frontend - Inicializando
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.7+ desde https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Navigate to frontend directory
cd /d "%~dp0frontend"

echo [INFO] Directorio actual: %CD%
echo [INFO] Iniciando servidor en http://localhost:8080
echo [INFO] Asegurate de que la API este corriendo en http://localhost:5000
echo.
echo ============================================
echo    Servidor Frontend Activo
echo ============================================
echo.
echo    URL: http://localhost:8080
echo    API: http://localhost:5000
echo.
echo    Presiona Ctrl+C para detener el servidor
echo ============================================
echo.

REM Start the server
python server.py

pause
