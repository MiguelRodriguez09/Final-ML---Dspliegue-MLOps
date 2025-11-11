# ===================================
# Setup Script - MLOps Project
# Purpose: Create Python virtual environment and install dependencies
# Location: scripts/set_up.ps1
# ===================================

Write-Host ""
Write-Host "=== Python Virtual Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# Guardar el directorio del script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Ir al directorio raíz del proyecto (un nivel arriba)
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

# Mostrar directorio de trabajo
Write-Host "Directorio de trabajo: $PWD" -ForegroundColor Yellow
Write-Host ""

# Desactivar el ambiente virtual actual si está activo
if ($env:VIRTUAL_ENV) {
    Write-Host "Desactivando ambiente virtual actual: $env:VIRTUAL_ENV" -ForegroundColor Yellow
    deactivate
}

Write-Host "Buscando código del proyecto en models\config.json..." -ForegroundColor Cyan

# Verificar que config.json existe
$ConfigPath = Join-Path $ProjectRoot "models\config.json"
if (-not (Test-Path $ConfigPath)) {
    Write-Host "ERROR: No se encontró models\config.json" -ForegroundColor Red
    Write-Host "Ruta esperada: $ConfigPath" -ForegroundColor Red
    Write-Host "Asegúrate de estar ejecutando el script desde la carpeta scripts/" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Leer project_code desde config.json
$ConfigContent = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$ProjectCode = $ConfigContent.project_code

# Verificar que se leyó el project_code
if (-not $ProjectCode) {
    Write-Host "ERROR: No se pudo leer project_code de config.json" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Código del proyecto: $ProjectCode" -ForegroundColor Green
Write-Host ""

# Verificar si el ambiente virtual ya existe
$VenvPath = Join-Path $ProjectRoot "$ProjectCode-venv"
if (Test-Path $VenvPath) {
    Write-Host "El ambiente virtual $ProjectCode-venv ya existe." -ForegroundColor Yellow
    $Recreate = Read-Host "¿Deseas eliminarlo y crear uno nuevo? (S/N)"
    if ($Recreate -eq "S" -or $Recreate -eq "s") {
        Write-Host "Eliminando ambiente virtual existente..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $VenvPath
        Write-Host "Ambiente eliminado." -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "Usando ambiente virtual existente." -ForegroundColor Green
        $SkipCreate = $true
    }
}

# Crear ambiente virtual si no existe
if (-not $SkipCreate) {
    Write-Host "Creando nuevo ambiente virtual: $ProjectCode-venv" -ForegroundColor Cyan
    python -m venv "$ProjectCode-venv"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Falló al crear el ambiente virtual." -ForegroundColor Red
        Write-Host "Verifica que Python esté instalado correctamente." -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

Write-Host "Activando ambiente virtual..." -ForegroundColor Cyan

# Activar ambiente virtual
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    & $ActivateScript
    
    Write-Host ""
    Write-Host "=== Ambiente virtual activado correctamente ===" -ForegroundColor Green
    Write-Host "Python actual:" -ForegroundColor Cyan
    Get-Command python | Select-Object -ExpandProperty Source
    Write-Host ""
    
    # Verificar si requirements.txt existe
    $RequirementsPath = Join-Path $ProjectRoot "requirements.txt"
    if (Test-Path $RequirementsPath) {
        Write-Host "=== Instalando requisitos ===" -ForegroundColor Cyan
        Write-Host "requirements.txt encontrado, instalando librerías..." -ForegroundColor Yellow
        Write-Host ""
        
        # Actualizar pip primero
        Write-Host "Actualizando pip..." -ForegroundColor Cyan
        python -m pip install --upgrade pip
        Write-Host ""
        
        # Instalar dependencias
        Write-Host "Instalando dependencias..." -ForegroundColor Cyan
        pip install --no-cache-dir -r $RequirementsPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "=== Todas las librerías instaladas correctamente ===" -ForegroundColor Green
            Write-Host ""

            # Registrar kernel de Jupyter
            Write-Host "=== Registrando ambiente virtual con Jupyter ===" -ForegroundColor Cyan
            Write-Host "Registrando kernel con Jupyter..." -ForegroundColor Yellow
            python -m ipykernel install --user --name="$ProjectCode-venv" --display-name="$ProjectCode-venv Python ETL"
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "=== Kernel de Jupyter registrado correctamente ===" -ForegroundColor Green
                Write-Host "Puedes seleccionar '$ProjectCode-venv Python ETL' en Jupyter notebook." -ForegroundColor Yellow
                Write-Host ""
            } else {
                Write-Host ""
                Write-Host "ADVERTENCIA: Falló al registrar el kernel de Jupyter." -ForegroundColor Yellow
                Write-Host "Jupyter notebook puede no reconocer este ambiente virtual." -ForegroundColor Yellow
                Write-Host ""
            }

            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "=== SETUP COMPLETADO EXITOSAMENTE ===" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Para activar el ambiente virtual en el futuro, ejecuta:" -ForegroundColor Cyan
            Write-Host "  .\$ProjectCode-venv\Scripts\Activate.ps1  (PowerShell)" -ForegroundColor Yellow
            Write-Host "  .\$ProjectCode-venv\Scripts\activate.bat  (CMD)" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Para desactivar el ambiente virtual:" -ForegroundColor Cyan
            Write-Host "  deactivate" -ForegroundColor Yellow
            Write-Host ""

        } else {
            Write-Host ""
            Write-Host "ERROR: Falló al instalar las librerías desde requirements.txt." -ForegroundColor Red
            Write-Host "Revisa los mensajes de error anteriores." -ForegroundColor Red
            Write-Host ""
        }
    } else {
        Write-Host ""
        Write-Host "ADVERTENCIA: requirements.txt no fue encontrado en el directorio raíz." -ForegroundColor Yellow
        Write-Host "Ruta esperada: $RequirementsPath" -ForegroundColor Yellow
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "ERROR: No se encontró el script de activación." -ForegroundColor Red
    Write-Host "Ruta esperada: $ActivateScript" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Presiona Enter para salir..." -ForegroundColor Cyan
Read-Host
