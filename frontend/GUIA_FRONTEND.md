# 🌐 Guía Completa del Frontend MLOps

## 📋 Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Frontend](#arquitectura-del-frontend)
3. [Guía de Inicio Rápido](#guía-de-inicio-rápido)
4. [Funcionalidades Detalladas](#funcionalidades-detalladas)
5. [Integración con la API](#integración-con-la-api)
6. [Personalización y Extensión](#personalización-y-extensión)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Resumen Ejecutivo

El **MLOps Frontend** es una interfaz web moderna, responsiva y completa para interactuar con el sistema de predicción de churn. Desarrollado con **HTML5**, **CSS3** y **JavaScript vanilla** (sin frameworks), consume la API Flask de manera eficiente y ofrece una experiencia de usuario intuitiva.

### Características Principales

✅ **3 Modos de Predicción**
- Individual: Formulario interactivo
- Por Lote: Carga de archivos CSV
- Datos de Prueba: Conjuntos predefinidos

✅ **Dashboard en Tiempo Real**
- Estado del sistema (API, modelo, preprocesador)
- Métricas del modelo (accuracy, ROC-AUC, F1-score)
- Historial de predicciones

✅ **Documentación Integrada**
- Información detallada del modelo
- Documentación de endpoints de API
- Ejemplos de uso con curl

✅ **Diseño Profesional**
- UI moderna con gradientes y sombras
- Totalmente responsivo (desktop, tablet, mobile)
- Animaciones suaves y transiciones
- Sistema de notificaciones

---

## 🏗️ Arquitectura del Frontend

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Port 8080)                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   index.html  │  │  styles.css  │  │    app.js    │      │
│  │              │  │              │  │              │      │
│  │  - Structure │  │  - Layout    │  │  - Logic     │      │
│  │  - Content   │  │  - Design    │  │  - API Calls │      │
│  │  - Semantic  │  │  - Colors    │  │  - State Mgmt│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│                         │ HTTP/JSON                          │
│                         ▼                                     │
├─────────────────────────────────────────────────────────────┤
│                      API (Port 5000)                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     GET /     │  │ GET /model-  │  │ POST /predict│      │
│  │              │  │     info     │  │              │      │
│  │ Health Check │  │ Model Metrics│  │  Prediction  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Usuario** interactúa con el frontend
2. **JavaScript** captura eventos y valida datos
3. **fetch()** envía petición HTTP a la API
4. **API Flask** procesa la petición
5. **Modelo ML** genera predicción
6. **Respuesta JSON** retorna al frontend
7. **Renderizado** muestra resultados al usuario

---

## 🚀 Guía de Inicio Rápido

### Paso 1: Verificar Requisitos

```bash
# Verificar Python instalado
python --version
# Output esperado: Python 3.x.x

# Verificar que la API esté corriendo
docker-compose ps
# mlops-api debe estar UP y HEALTHY
```

### Paso 2: Iniciar el Frontend

**Opción A: Script Automatizado (Recomendado)**

```bash
# Ejecutar el launcher
.\start_frontend.bat
```

**Opción B: Manual**

```bash
# Navegar al directorio frontend
cd frontend

# Iniciar servidor Python
python server.py
```

### Paso 3: Abrir en el Navegador

```
http://localhost:8080
```

### Paso 4: Realizar Primera Predicción

1. **Navegar** a la sección "Predicción"
2. **Completar** el formulario con datos del cliente
3. **Hacer clic** en "Predecir"
4. **Visualizar** resultados con probabilidad

---

## 🎨 Funcionalidades Detalladas

### 1. 📊 Dashboard Principal

#### A. Estado del Sistema

Muestra en tiempo real:
- **API Status**: Conectado/Desconectado
- **Modelo**: Cargado/No Cargado
- **Preprocesador**: Cargado/No Cargado

**Actualización**: Automática al cargar la página

#### B. Métricas del Modelo

Visualiza las métricas de performance:
- **Accuracy**: 87.05%
- **ROC-AUC**: 86.58%
- **F1-Score**: 60.82%
- **CV Mean**: 86.18%

**Fuente**: Endpoint `/model-info`

#### C. Historial de Predicciones

Lista las últimas 10 predicciones:
- Timestamp
- Predicción (CHURN/NO CHURN)
- Probabilidad

**Almacenamiento**: LocalStorage del navegador

---

### 2. 🔮 Predicción Individual

#### Formulario Interactivo

**Columna 1: Información Personal**
```
Credit Score     [300-850]
País             [France/Spain/Germany]
Género           [Male/Female]
Edad             [18-100]
```

**Columna 2: Información Bancaria**
```
Años como Cliente [0-10]
Balance ($)       [0+]
Núm. Productos    [1-4]
Salario ($)       [0+]
```

**Columna 3: Estado del Cliente**
```
☑ Tiene Tarjeta de Crédito
☑ Miembro Activo
```

#### Botones de Acción

- **Limpiar**: Resetea todos los campos
- **Datos de Ejemplo**: Carga valores de muestra
- **Predecir**: Envía a la API y muestra resultado

#### Visualización de Resultados

```
┌─────────────────────────────────────────┐
│         PREDICCIÓN: CHURN/NO CHURN      │
│                                         │
│              🔴 / 🟢                    │
│              XX.X%                      │
│                                         │
│  ████████████████░░░░░ 75%             │
│                                         │
│  Credit Score: XXX    Balance: $XXX    │
│  Edad: XX años        Productos: X     │
│  Antigüedad: X        Salario: $XXX    │
└─────────────────────────────────────────┘
```

---

### 3. 📁 Predicción por Lote

#### Carga de Archivos CSV

**Métodos de Carga:**
1. **Drag & Drop**: Arrastra el archivo a la zona
2. **Click**: Selecciona archivo desde explorador

**Formato Requerido:**
```csv
CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary
619,France,Female,42,2,0,1,1,1,101348.88
608,Spain,Female,41,1,83807.86,1,0,1,112542.58
```

#### Descarga de Plantilla

- Click en "Descargar Plantilla"
- Obtiene archivo `template.csv` con formato correcto

#### Resultados por Lote

**Panel de Estadísticas:**
- Total Procesados: X
- Predicción CHURN: X
- Predicción NO CHURN: X
- Probabilidad Promedio: XX%

**Tabla de Resultados:**
```
# | Predicción | Probabilidad | Visualización
--+------------+--------------+---------------
1 | CHURN      | 75.3%        | ████████░░
2 | NO CHURN   | 25.1%        | ███░░░░░░░
```

**Acciones:**
- Descargar Resultados (CSV)
- Filtrar por predicción
- Ordenar por probabilidad

---

### 4. 🧪 Datos de Prueba

#### Conjuntos Predefinidos

**1. Cliente Premium**
- Credit Score: 850
- Balance: $150,000
- Productos: 3
- **Esperado**: Baja probabilidad de churn

**2. Cliente Estándar**
- Credit Score: 650
- Balance: $80,000
- Productos: 2
- **Esperado**: Probabilidad media

**3. Cliente en Riesgo**
- Credit Score: 400
- Balance: $0
- Productos: 1
- **Esperado**: Alta probabilidad de churn

**Uso:**
1. Click en tarjeta de test
2. Datos se cargan automáticamente en formulario
3. Click "Predecir" para ver resultado

---

### 5. ℹ️ Información del Modelo

#### Panel de Detalles

**Información Básica:**
- Nombre: Gradient Boosting
- Tipo: GradientBoostingClassifier
- Características: 11

**Métricas de Performance:**
```
┌────────────────┬──────────┐
│ Test Accuracy  │  87.05%  │
│ Test F1-Score  │  60.82%  │
│ Test ROC-AUC   │  86.58%  │
│ CV Mean Score  │  86.18%  │
└────────────────┴──────────┘
```

**Características del Modelo:**
- ✅ Gradient Boosting Classifier
- ✅ Entrenado con 11 características
- ✅ Cross-validation con 5 folds
- ✅ Optimización de hiperparámetros

---

### 6. 📚 Documentación de API

#### Endpoints Disponibles

**1. Health Check**
```http
GET /
```
**Respuesta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true
}
```

**2. Model Info**
```http
GET /model-info
```
**Respuesta:**
```json
{
  "model_name": "Gradient Boosting",
  "model_type": "GradientBoostingClassifier",
  "n_features": 11,
  "metrics": { ... }
}
```

**3. Predict**
```http
POST /predict
Content-Type: application/json

{
  "CreditScore": 619,
  "Geography": "France",
  "Gender": "Female",
  ...
}
```

**Respuesta:**
```json
{
  "prediction": 1,
  "churn_probability": 0.753
}
```

---

## 🔌 Integración con la API

### Configuración de Conexión

**Archivo:** `static/js/app.js`

```javascript
const API_BASE_URL = 'http://localhost:5000';
```

### Funciones de API

#### checkSystemStatus()
```javascript
// Verifica estado del sistema
// Endpoint: GET /
// Actualiza: sidebar status
```

#### loadModelInfo()
```javascript
// Carga información del modelo
// Endpoint: GET /model-info
// Actualiza: sección de modelo
```

#### makePrediction(inputData)
```javascript
// Realiza predicción individual
// Endpoint: POST /predict
// Parámetros: objeto con datos del cliente
// Retorna: { prediction, churn_probability }
```

#### makeBatchPrediction(batchData)
```javascript
// Realiza predicción por lote
// Endpoint: POST /predict-batch
// Parámetros: array de objetos
// Retorna: { predictions: [...] }
```

### Manejo de Errores

```javascript
try {
  const result = await makePrediction(data);
  renderPredictionResult(result);
} catch (error) {
  showError('Error al realizar predicción');
  console.error(error);
}
```

### CORS

La API debe tener CORS habilitado:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

---

## 🎨 Personalización y Extensión

### Cambiar Colores

**Archivo:** `static/css/styles.css`

```css
:root {
    --primary-color: #2563eb;      /* Azul */
    --secondary-color: #10b981;    /* Verde */
    --danger-color: #ef4444;       /* Rojo */
    --success-color: #10b981;      /* Verde */
}
```

### Agregar Nueva Sección

**1. HTML (index.html):**
```html
<section id="nueva-seccion" class="section">
    <h2>Nueva Sección</h2>
    <p>Contenido...</p>
</section>
```

**2. Navegación:**
```html
<a href="#nueva-seccion" class="nav-link">
    <i class="fas fa-icon"></i> Nueva
</a>
```

**3. JavaScript:**
```javascript
// Agregar lógica en app.js
function handleNuevaSeccion() {
    // Tu código aquí
}
```

### Agregar Nuevo Gráfico

**Opción 1: Chart.js**

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

```javascript
const ctx = document.getElementById('myChart');
new Chart(ctx, {
    type: 'bar',
    data: { ... }
});
```

**Opción 2: D3.js** (visualizaciones avanzadas)

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

### Agregar Autenticación

```javascript
// En app.js
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('authToken');
    
    return fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Authorization': `Bearer ${token}`,
            ...options.headers
        }
    });
}
```

---

## 🔧 Troubleshooting

### Problema 1: "No se pudo conectar con la API"

**Síntomas:**
- Status: Desconectado
- Métricas no cargan
- Predicciones fallan

**Diagnóstico:**
```bash
# Verificar que la API esté corriendo
docker-compose ps

# Verificar logs
docker-compose logs mlops-api

# Test manual
curl http://localhost:5000/
```

**Solución:**
1. Iniciar API: `docker-compose up -d`
2. Verificar URL en `app.js`
3. Verificar CORS en API

---

### Problema 2: CORS Error

**Síntomas:**
```
Access to fetch at 'http://localhost:5000' from origin 'http://localhost:8080' 
has been blocked by CORS policy
```

**Solución:**

En `model_deploy.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Agregar esta línea
```

Reiniciar API:
```bash
docker-compose restart mlops-api
```

---

### Problema 3: Estilos no Cargan

**Síntomas:**
- Página sin estilos
- Layout roto

**Solución:**

1. **No abrir HTML directamente** (file://)
2. **Usar servidor HTTP**:
   ```bash
   python -m http.server 8080
   ```
3. **Verificar rutas** en index.html:
   ```html
   <link rel="stylesheet" href="static/css/styles.css">
   ```

---

### Problema 4: CSV no Procesa

**Síntomas:**
- Error al subir CSV
- "Error al procesar archivo"

**Solución:**

1. **Verificar formato** del CSV
2. **Comprobar separador**: debe ser coma (,)
3. **Verificar headers**: deben coincidir exactamente
4. **Revisar encoding**: UTF-8

**CSV Válido:**
```csv
CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary
619,France,Female,42,2,0,1,1,1,101348.88
```

---

### Problema 5: Formulario no Envía

**Síntomas:**
- Click en "Predecir" no hace nada
- Consola muestra errores

**Diagnóstico:**
```javascript
// Abrir consola del navegador (F12)
// Buscar errores en rojo
```

**Solución:**

1. **Verificar todos los campos** están completos
2. **Comprobar validaciones** HTML5
3. **Revisar formato** de datos en app.js
4. **Test en consola**:
   ```javascript
   console.log(document.getElementById('predictionForm'));
   ```

---

## 📊 Métricas y Monitoreo

### Performance del Frontend

**Lighthouse Score Objetivo:**
- Performance: 90+
- Accessibility: 95+
- Best Practices: 90+
- SEO: 85+

### Métricas Clave

```javascript
// Tiempo de carga
window.addEventListener('load', () => {
    console.log(`Página cargada en ${performance.now()}ms`);
});

// Tiempo de API call
console.time('API Call');
await makePrediction(data);
console.timeEnd('API Call');
```

---

## 🚀 Deploy en Producción

### Checklist Pre-Deploy

- [ ] Cambiar `API_BASE_URL` a URL de producción
- [ ] Minificar CSS y JavaScript
- [ ] Optimizar imágenes
- [ ] Habilitar HTTPS
- [ ] Configurar CDN
- [ ] Setup de monitoreo
- [ ] Implementar analytics

### Deploy en Vercel

```bash
npm i -g vercel
cd frontend
vercel --prod
```

### Deploy en Netlify

```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod --dir=.
```

### Deploy con Docker

```dockerfile
FROM nginx:alpine
COPY frontend /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
docker build -t mlops-frontend .
docker run -d -p 80:80 mlops-frontend
```

---

## 📚 Recursos Adicionales

### Documentación
- [Flask CORS](https://flask-cors.readthedocs.io/)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [CSS Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)

### Herramientas
- [Postman](https://www.postman.com/) - Testing de API
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/) - Debugging
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance

### Librerías Recomendadas
- [Chart.js](https://www.chartjs.org/) - Gráficos
- [Alpine.js](https://alpinejs.dev/) - Reactividad ligera
- [Tailwind CSS](https://tailwindcss.com/) - CSS utility-first

---

## 📞 Soporte

¿Problemas? ¿Sugerencias?

- 📧 Email: soporte@mlops.com
- 🐛 Issues: GitHub Issues
- 💬 Chat: Discord/Slack
- 📖 Docs: Wiki del proyecto

---

**Desarrollado con ❤️ para el proyecto MLOps**
