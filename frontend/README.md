# 🎨 MLOps Frontend - Interfaz de Usuario

Frontend moderno y responsivo para consumir la API de predicción de churn del proyecto MLOps.

## 🚀 Características

- ✅ **Predicción Individual**: Formulario interactivo para predecir churn de un cliente
- ✅ **Predicción por Lote**: Carga de archivos CSV para predicciones masivas
- ✅ **Datos de Prueba**: Conjuntos de datos predefinidos para testing rápido
- ✅ **Dashboard en Tiempo Real**: Visualización del estado del sistema y métricas del modelo
- ✅ **Historial de Predicciones**: Registro de las últimas 10 predicciones realizadas
- ✅ **Documentación de API**: Referencia completa de endpoints disponibles
- ✅ **Diseño Responsivo**: Compatible con dispositivos móviles y tablets
- ✅ **Notificaciones**: Sistema de alertas para feedback del usuario

## 📁 Estructura del Proyecto

```
frontend/
├── index.html              # Página principal
├── static/
│   ├── css/
│   │   └── styles.css     # Estilos CSS personalizados
│   └── js/
│       └── app.js         # Lógica JavaScript
├── README.md              # Este archivo
└── server.py              # Servidor HTTP simple (opcional)
```

## 🛠️ Instalación y Uso

### Opción 1: Servidor HTTP Simple con Python

```bash
# Navegar al directorio frontend
cd frontend

# Python 3
python -m http.server 8080

# O usar el servidor incluido
python server.py
```

Luego abre tu navegador en: **http://localhost:8080**

### Opción 2: Live Server (VS Code)

1. Instala la extensión "Live Server" en VS Code
2. Clic derecho en `index.html`
3. Selecciona "Open with Live Server"

### Opción 3: Servidor Web (Producción)

Puedes servir los archivos con cualquier servidor web:

- **Nginx**
- **Apache**
- **Node.js (Express)**
- **Vercel / Netlify** (Deploy estático)

## 🔧 Configuración

### Configurar la URL de la API

Edita el archivo `static/js/app.js` y modifica la constante `API_BASE_URL`:

```javascript
const API_BASE_URL = 'http://localhost:5000'; // Cambiar según tu configuración
```

### Para Producción

Si tu API está en un dominio diferente, actualiza la URL:

```javascript
const API_BASE_URL = 'https://tu-api.com';
```

## 📊 Uso del Frontend

### 1. Predicción Individual

1. Completa el formulario con los datos del cliente
2. Haz clic en "Predecir"
3. Visualiza los resultados con probabilidad y detalles

**Campos requeridos:**
- Credit Score (300-850)
- País (France, Spain, Germany)
- Género (Male, Female)
- Edad (18-100)
- Años como Cliente (0-10)
- Balance ($)
- Número de Productos (1-4)
- Tiene Tarjeta de Crédito (Sí/No)
- Miembro Activo (Sí/No)
- Salario Estimado ($)

### 2. Predicción por Lote

1. Prepara un archivo CSV con las columnas requeridas
2. Arrastra el archivo o haz clic para seleccionar
3. Visualiza resultados en tabla con estadísticas

**Formato del CSV:**
```csv
CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary
619,France,Female,42,2,0,1,1,1,101348.88
608,Spain,Female,41,1,83807.86,1,0,1,112542.58
```

Puedes descargar una plantilla de ejemplo desde la interfaz.

### 3. Datos de Prueba

Haz clic en una de las tarjetas predefinidas:

- **Cliente Premium**: Alto balance, múltiples productos
- **Cliente Estándar**: Balance medio, cliente activo
- **Cliente en Riesgo**: Bajo balance, inactivo

## 🎨 Personalización

### Colores

Edita las variables CSS en `static/css/styles.css`:

```css
:root {
    --primary-color: #2563eb;      /* Color principal */
    --secondary-color: #10b981;    /* Color secundario */
    --danger-color: #ef4444;       /* Color de alerta */
    --success-color: #10b981;      /* Color de éxito */
}
```

### Logo y Branding

1. Reemplaza el icono en el header (línea 16 de `index.html`)
2. Actualiza el título del proyecto
3. Modifica el footer con tus enlaces

## 📱 Características Responsivas

El frontend está optimizado para:

- 💻 **Desktop**: Vista completa con sidebar y contenido principal
- 📱 **Tablet**: Layout adaptativo con columnas ajustadas
- 📲 **Mobile**: Diseño apilado con navegación optimizada

## 🔌 API Endpoints Consumidos

El frontend consume los siguientes endpoints:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check del sistema |
| GET | `/model-info` | Información y métricas del modelo |
| POST | `/predict` | Predicción individual |
| POST | `/predict-batch` | Predicción por lote |

## 🐛 Solución de Problemas

### Error: "No se pudo conectar con la API"

**Causa**: La API Flask no está corriendo o hay problemas de CORS.

**Solución**:
1. Verifica que la API esté corriendo: `docker-compose ps`
2. Verifica la URL en `app.js`
3. Asegúrate que CORS esté habilitado en Flask

### Error: "Failed to fetch"

**Causa**: Problema de CORS o URL incorrecta.

**Solución**:
```python
# En model_deploy.py, agregar:
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS
```

### La página no carga los estilos

**Causa**: Rutas incorrectas o servidor no configurado.

**Solución**:
- Verifica que la estructura de carpetas sea correcta
- Usa un servidor HTTP (no abras el HTML directamente)
- Revisa la consola del navegador para errores

## 🚀 Deploy en Producción

### Vercel

```bash
# Instalar Vercel CLI
npm i -g vercel

# Desplegar
cd frontend
vercel
```

### Netlify

1. Arrastra la carpeta `frontend` a Netlify Drop
2. O usa Netlify CLI:

```bash
npm install -g netlify-cli
netlify deploy --prod --dir=frontend
```

### Nginx

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    root /var/www/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] Exportación de resultados a PDF
- [ ] Gráficos interactivos con Chart.js o D3.js
- [ ] Comparación de predicciones
- [ ] Filtros avanzados en historial
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)
- [ ] Progressive Web App (PWA)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es parte del sistema MLOps de predicción de churn.

## 👥 Autor

Desarrollado como parte del proyecto Final-ML---Dspliegue-MLOps

---

**¿Necesitas ayuda?** Abre un issue en el repositorio de GitHub.
