# 🔍 Integración con SonarCloud

## 📋 Descripción

Este proyecto está integrado con **SonarCloud** para análisis continuo de calidad de código. SonarCloud proporciona:

- 🐛 Detección de bugs
- 🔒 Identificación de vulnerabilidades de seguridad
- 📊 Métricas de calidad de código
- 💡 Code smells y deuda técnica
- 📈 Cobertura de tests
- 🎯 Quality Gates

---

## 🚀 Configuración Inicial

### 1. Crear cuenta en SonarCloud

1. Ve a [sonarcloud.io](https://sonarcloud.io)
2. Inicia sesión con tu cuenta de GitHub
3. Autoriza a SonarCloud para acceder a tus repositorios

### 2. Importar el repositorio

1. Haz clic en el botón **"+"** → **"Analyze new project"**
2. Selecciona el repositorio: `MiguelRodriguez09/Final-ML---Dspliegue-MLOps`
3. Haz clic en **"Set Up"**

### 3. Configurar la organización

- **Organization Key**: `miguelrodriguez09`
- **Project Key**: `MiguelRodriguez09_Final-ML---Dspliegue-MLOps`

### 4. Obtener el token de SonarCloud

1. En SonarCloud, ve a **"My Account"** → **"Security"**
2. Genera un nuevo token:
   - **Name**: `GitHub Actions - Final ML`
   - **Type**: `Global Analysis Token`
   - **Expires in**: 90 days (o sin expiración)
3. Copia el token generado

### 5. Agregar el token a GitHub Secrets

1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Haz clic en **"New repository secret"**
4. Agrega el secreto:
   - **Name**: `SONAR_TOKEN`
   - **Value**: [pega el token de SonarCloud]
5. Haz clic en **"Add secret"**

---

## 📁 Archivos de Configuración

### `sonar-project.properties`

Configuración principal del análisis:

```properties
sonar.projectKey=MiguelRodriguez09_Final-ML---Dspliegue-MLOps
sonar.organization=miguelrodriguez09
sonar.projectName=Final-ML-Despliegue-MLOps
sonar.sources=mlops_pipeline/src
sonar.python.version=3.13
```

### `.github/workflows/sonarcloud.yml`

GitHub Action que ejecuta el análisis en cada push o PR:

- ✅ Se ejecuta automáticamente en push a `main` o `dev`
- ✅ Se ejecuta en cada Pull Request
- ✅ Usa el token de `SONAR_TOKEN` de los secrets

### `.sonarignore`

Archivos y carpetas excluidos del análisis:

- Entorno virtual (`Proyecto-venv/`)
- Archivos de datos (`mlops_pipeline/data/`)
- Modelos entrenados (`mlops_pipeline/models/`)
- Cache de Python (`__pycache__/`)

---

## 🔄 Flujo de Trabajo

### Análisis Automático

Cada vez que hagas un push o PR, GitHub Actions ejecutará:

1. **Checkout** del código
2. **Setup** de Python 3.13
3. **Instalación** de dependencias
4. **Análisis** con SonarCloud
5. **Reporte** de resultados

### Ver Resultados

1. Ve a [sonarcloud.io](https://sonarcloud.io)
2. Selecciona tu organización y proyecto
3. Revisa:
   - **Overview**: Resumen de métricas
   - **Issues**: Bugs, vulnerabilidades, code smells
   - **Measures**: Métricas detalladas
   - **Activity**: Historial de análisis

---

## 📊 Métricas Principales

### Reliability (Confiabilidad)
- **Bugs**: Número de errores detectados
- **Rating**: A (mejor) a E (peor)

### Security (Seguridad)
- **Vulnerabilities**: Vulnerabilidades de seguridad
- **Security Hotspots**: Puntos sensibles
- **Rating**: A (mejor) a E (peor)

### Maintainability (Mantenibilidad)
- **Code Smells**: Problemas de calidad de código
- **Technical Debt**: Tiempo estimado para resolver issues
- **Rating**: A (mejor) a E (peor)

### Coverage (Cobertura)
- **Test Coverage**: % de código cubierto por tests
- **Lines to Cover**: Líneas que deberían tener tests

### Duplications (Duplicación)
- **Duplicated Lines**: Líneas de código duplicadas
- **Duplicated Blocks**: Bloques duplicados

---

## 🎯 Quality Gate

### Condiciones por Defecto

El Quality Gate evalúa:

- ✅ **Coverage on New Code** ≥ 80%
- ✅ **Duplicated Lines on New Code** ≤ 3%
- ✅ **Maintainability Rating on New Code** = A
- ✅ **Reliability Rating on New Code** = A
- ✅ **Security Rating on New Code** = A

### Personalizar Quality Gate

1. En SonarCloud → **Quality Gates**
2. Crea un nuevo Quality Gate personalizado
3. Define tus propias condiciones
4. Asígnalo a tu proyecto

---

## 🛠️ Comandos Locales

### Ejecutar análisis local (opcional)

```bash
# Instalar SonarScanner
npm install -g sonarqube-scanner

# Ejecutar análisis
sonar-scanner \
  -Dsonar.projectKey=MiguelRodriguez09_Final-ML---Dspliegue-MLOps \
  -Dsonar.organization=miguelrodriguez09 \
  -Dsonar.sources=mlops_pipeline/src \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=$SONAR_TOKEN
```

---

## 🔧 Resolución de Problemas

### Error: "No analysis found"

**Causa**: El análisis no se ha ejecutado aún.

**Solución**: Haz un push al repositorio para disparar el workflow.

### Error: "SONAR_TOKEN not found"

**Causa**: El token no está configurado en GitHub Secrets.

**Solución**: Agrega el token siguiendo el paso 5 de la configuración.

### Warning: "File not found"

**Causa**: Archivos excluidos en `.sonarignore` o no existen.

**Solución**: Verifica las rutas en `sonar-project.properties`.

---

## 📈 Buenas Prácticas

### 1. Revisar Issues Regularmente

- Revisa el dashboard de SonarCloud semanalmente
- Prioriza bugs y vulnerabilidades de seguridad
- Resuelve code smells importantes

### 2. Mantener Quality Gate Verde

- Asegúrate de que el Quality Gate pase en cada PR
- No hagas merge si el Quality Gate falla
- Corrige issues antes de hacer merge

### 3. Aumentar Cobertura de Tests

- Escribe tests para código nuevo
- Apunta a ≥80% de cobertura
- Usa `pytest-cov` para medir cobertura localmente

### 4. Evitar Duplicación de Código

- Refactoriza código duplicado
- Usa funciones y clases reutilizables
- Aplica principios DRY (Don't Repeat Yourself)

---

## 🔗 Enlaces Útiles

- 📚 [Documentación de SonarCloud](https://docs.sonarcloud.io/)
- 🐙 [SonarCloud GitHub Action](https://github.com/SonarSource/sonarcloud-github-action)
- 🐍 [Análisis de Python en SonarCloud](https://docs.sonarcloud.io/advanced-setup/languages/python/)
- 🎯 [Quality Gates](https://docs.sonarcloud.io/improving/quality-gates/)

---

## 📝 Configuración del Proyecto

### Información del Proyecto

- **Organización**: `miguelrodriguez09`
- **Project Key**: `MiguelRodriguez09_Final-ML---Dspliegue-MLOps`
- **Nombre**: `Final-ML-Despliegue-MLOps`
- **Lenguaje**: Python 3.13
- **Directorio de código**: `mlops_pipeline/src/`

### Exclusiones

```
- Proyecto-venv/
- __pycache__/
- .ipynb_checkpoints/
- *.ipynb
- mlops_pipeline/data/
- mlops_pipeline/models/
- mlops_pipeline/reports/
- mlops_pipeline/monitoring/
```

---

## ✅ Checklist de Integración

- [x] Cuenta de SonarCloud creada
- [x] Repositorio importado
- [x] Token generado
- [x] Token agregado a GitHub Secrets
- [x] `sonar-project.properties` configurado
- [x] `.sonarignore` creado
- [x] GitHub Action configurado
- [x] `.gitignore` actualizado
- [ ] Primer análisis ejecutado
- [ ] Quality Gate configurado
- [ ] Badge agregado al README

---

## 🏷️ Badge de SonarCloud

Agrega este badge a tu `README.md`:

```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MiguelRodriguez09_Final-ML---Dspliegue-MLOps&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MiguelRodriguez09_Final-ML---Dspliegue-MLOps)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MiguelRodriguez09_Final-ML---Dspliegue-MLOps&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MiguelRodriguez09_Final-ML---Dspliegue-MLOps)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=MiguelRodriguez09_Final-ML---Dspliegue-MLOps&metric=bugs)](https://sonarcloud.io/summary/new_code?id=MiguelRodriguez09_Final-ML---Dspliegue-MLOps)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=MiguelRodriguez09_Final-ML---Dspliegue-MLOps&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=MiguelRodriguez09_Final-ML---Dspliegue-MLOps)
```

---

**¡Listo! Tu proyecto ahora está integrado con SonarCloud para análisis continuo de calidad de código.** 🎉
