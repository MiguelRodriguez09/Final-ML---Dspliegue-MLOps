@echo off
REM ============================================
REM MLOps - Launcher Completo (API + Frontend)
REM ============================================

echo.
echo ============================================
echo      MLOps System - Inicializacion
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Check if Docker containers are running
echo [INFO] Verificando contenedores Docker...
docker ps --filter "name=mlops-api" --format "{{.Status}}" | findstr /C:"Up" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================
    echo    OPCION 1: Usar Docker (Recomendado)
    echo ============================================
    echo.
    echo Los contenedores no estan corriendo.
    echo.
    echo Para iniciar con Docker:
    echo   docker-compose up -d
    echo.
    echo Luego ejecuta este script nuevamente.
    echo.
    echo ============================================
    echo    OPCION 2: Ejecutar sin Docker
    echo ============================================
    echo.
    choice /C SN /M "Deseas iniciar sin Docker (API local + Frontend)"
    if errorlevel 2 goto :exit
    if errorlevel 1 goto :local
) else (
    echo [OK] Contenedores Docker corriendo
    echo.
    goto :frontend_only
)

:local
echo.
echo ============================================
echo   Iniciando API Local (Puerto 5000)
echo ============================================
echo.

REM Start API in background
start "MLOps API" cmd /c "python mlops_pipeline/src/model_deploy.py"
echo [OK] API iniciada en segundo plano
timeout /t 5 /nobreak >nul

goto :frontend_only

:frontend_only
echo.
echo ============================================
echo   Iniciando Frontend (Puerto 8080)
echo ============================================
echo.

REM Start Frontend
cd frontend
start "MLOps Frontend" cmd /c "python server.py"
echo [OK] Frontend iniciado en segundo plano
cd ..

timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo        SISTEMA MLOPS INICIADO
echo ============================================
echo.
echo  API:       http://localhost:5000
echo  Frontend:  http://localhost:8080
echo.
echo  Dashboard: http://localhost:8501 (si Docker esta activo)
echo.
echo ============================================
echo.
echo [INFO] Abriendo navegador...
timeout /t 2 /nobreak >nul

REM Open browser
start http://localhost:8080

echo.
echo [OK] Sistema iniciado correctamente
echo.
echo Presiona cualquier tecla para ver instrucciones...
pause >nul

echo.
echo ============================================
echo          INSTRUCCIONES DE USO
echo ============================================
echo.
echo 1. El navegador deberia abrirse automaticamente
echo    Si no, abre: http://localhost:8080
echo.
echo 2. Usa la interfaz para hacer predicciones:
echo    - Tab "Prediccion Individual": Formulario interactivo
echo    - Tab "Prediccion por Lote": Carga CSV
echo    - Tab "Datos de Prueba": Conjuntos predefinidos
echo.
echo 3. Para detener los servicios:
echo    - Cierra las ventanas de terminal
echo    - O presiona Ctrl+C en cada ventana
echo.
echo ============================================
echo.

:exit
pause
