@echo off
REM ===================================
REM Setup Script - MLOps Project
REM Purpose: Create Python virtual environment and install dependencies
REM Location: scripts/set_up.bat
REM ===================================

echo.
echo === Python Virtual Environment Setup ===
echo.

REM Guardar el directorio actual (scripts/)
set SCRIPT_DIR=%~dp0

REM Ir al directorio raíz del proyecto (un nivel arriba)
cd /d "%SCRIPT_DIR%.."

REM Mostrar directorio de trabajo
echo Directorio de trabajo: %CD%
echo.

REM Desactivar el ambiente virtual actual si está activo
if defined VIRTUAL_ENV (
    echo Desactivando ambiente virtual actual: %VIRTUAL_ENV%
    call deactivate
)

echo Buscando codigo del proyecto en models\config.json...

setlocal EnableDelayedExpansion

REM Verificar que config.json existe
if not exist "models\config.json" (
    echo ERROR: No se encontro models\config.json
    echo Asegurate de estar ejecutando el script desde la carpeta scripts/
    pause
    exit /b 1
)

REM Leer línea que contiene "project_code"
for /f "usebackq tokens=2 delims=:" %%A in (`findstr "project_code" models\config.json`) do (
    set "line=%%A"
    set "line=!line:,=!"
    set "line=!line:"=!"
    set "line=!line:~1!"
    set "project_code=!line!"
)

REM Verificar que se leyó el project_code
if "!project_code!"=="" (
    echo ERROR: No se pudo leer project_code de config.json
    pause
    exit /b 1
)

echo Codigo del proyecto: !project_code!
echo.

REM Verificar si el ambiente virtual ya existe
if exist "!project_code!-venv\" (
    echo El ambiente virtual !project_code!-venv ya existe.
    echo ¿Deseas eliminarlo y crear uno nuevo? (S/N^)
    set /p "RECREATE="
    if /i "!RECREATE!"=="S" (
        echo Eliminando ambiente virtual existente...
        rmdir /s /q "!project_code!-venv"
        echo Ambiente eliminado.
        echo.
    ) else (
        echo Usando ambiente virtual existente.
        goto ACTIVATE_ENV
    )
)

echo Creando nuevo ambiente virtual: !project_code!-venv
py -m venv !project_code!-venv

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al crear el ambiente virtual.
    echo Verifica que Python este instalado correctamente.
    pause
    exit /b 1
)

:ACTIVATE_ENV
echo Activando ambiente virtual...
call !project_code!-venv\Scripts\activate

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Ambiente virtual activado correctamente ===
    echo Python actual: 
    where python
    echo.
    
    echo === Instalando requisitos ===
    if exist requirements.txt (
        echo requirements.txt encontrado, instalando librerias...
        echo.
        
        REM Actualizar pip primero
        echo Actualizando pip...
        python -m pip install --upgrade pip
        echo.
        
        REM Instalar dependencias
        echo Instalando dependencias...
        pip install --no-cache-dir -r requirements.txt
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo === Todas las librerias instaladas correctamente ===
            echo.

            echo === Registrando ambiente virtual con Jupyter ===
            echo Registrando kernel con Jupyter...
            python -m ipykernel install --user --name=!project_code!-venv --display-name="!project_code!-venv Python ETL"
            
            if %ERRORLEVEL% EQU 0 (
                echo.
                echo === Kernel de Jupyter registrado correctamente ===
                echo Puedes seleccionar "!project_code!-venv Python ETL" en Jupyter notebook.
                echo.
            ) else (
                echo.
                echo ADVERTENCIA: Fallo al registrar el kernel de Jupyter.
                echo Jupyter notebook puede no reconocer este ambiente virtual.
                echo.
            )

            echo.
            echo ========================================
            echo === SETUP COMPLETADO EXITOSAMENTE ===
            echo ========================================
            echo.
            echo Para activar el ambiente virtual en el futuro, ejecuta:
            echo   .\!project_code!-venv\Scripts\Activate.ps1  (PowerShell^)
            echo   .\!project_code!-venv\Scripts\activate.bat  (CMD^)
            echo.
            echo Para desactivar el ambiente virtual:
            echo   deactivate
            echo.

        ) else (
            echo.
            echo ERROR: Fallo al instalar las librerias desde requirements.txt.
            echo Revisa los mensajes de error anteriores.
            echo.
        )
    ) else (
        echo.
        echo ADVERTENCIA: requirements.txt no fue encontrado en el directorio raiz.
        echo Ruta esperada: %CD%\requirements.txt
        echo.
    )
) else (
    echo.
    echo ERROR: Fallo al activar el ambiente virtual.
    echo.
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
