// ============================================
// MLOps Frontend - JavaScript
// ============================================

// API Configuration
// Detectar si estamos en Docker o local
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'  // Desarrollo local
    : 'http://localhost:5000';  // Producción (cambiar si es necesario)

// State Management
const state = {
    predictions: [],
    modelInfo: null,
    systemStatus: null
};

// Test Data Samples
const testDataSamples = [
    {
        name: 'Cliente Premium',
        data: {
            CreditScore: 850,
            Geography: 'France',
            Gender: 'Male',
            Age: 45,
            Tenure: 10,
            Balance: 150000,
            NumOfProducts: 3,
            HasCrCard: 1,
            IsActiveMember: 1,
            EstimatedSalary: 200000
        }
    },
    {
        name: 'Cliente Estándar',
        data: {
            CreditScore: 650,
            Geography: 'Spain',
            Gender: 'Female',
            Age: 35,
            Tenure: 5,
            Balance: 80000,
            NumOfProducts: 2,
            HasCrCard: 1,
            IsActiveMember: 1,
            EstimatedSalary: 75000
        }
    },
    {
        name: 'Cliente en Riesgo',
        data: {
            CreditScore: 400,
            Geography: 'Germany',
            Gender: 'Male',
            Age: 55,
            Tenure: 1,
            Balance: 0,
            NumOfProducts: 1,
            HasCrCard: 0,
            IsActiveMember: 0,
            EstimatedSalary: 30000
        }
    }
];

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});

function initApp() {
    console.log('Initializing MLOps Frontend...');
    
    // Setup event listeners
    setupEventListeners();
    
    // Load initial data
    checkSystemStatus();
    loadModelInfo();
    loadModelMetrics();
    
    // Setup file upload
    setupFileUpload();
    
    console.log('App initialized successfully');
}

// ============================================
// Event Listeners
// ============================================
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavigation);
    });
    
    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', handleTabChange);
    });
    
    // Form submission
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', handlePredictionSubmit);
    }
}

function handleNavigation(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href').substring(1);
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    this.classList.add('active');
    
    // Show target section
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(targetId).classList.add('active');
}

function handleTabChange(e) {
    const targetTab = this.getAttribute('data-tab');
    
    // Update active tab button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    this.classList.add('active');
    
    // Show target tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(targetTab).classList.add('active');
}

// ============================================
// API Calls
// ============================================
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

async function checkSystemStatus() {
    try {
        const data = await apiCall('/');
        state.systemStatus = data;
        renderSystemStatus(data);
    } catch (error) {
        renderSystemStatus({ status: 'error', message: 'No se pudo conectar con la API' });
    }
}

async function loadModelInfo() {
    try {
        const data = await apiCall('/model-info');
        state.modelInfo = data;
        renderModelInfo(data);
    } catch (error) {
        console.error('Failed to load model info:', error);
        document.getElementById('modelInfoContent').innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                Error al cargar la información del modelo
            </div>
        `;
    }
}

async function loadModelMetrics() {
    try {
        const data = await apiCall('/model-info');
        renderModelMetrics(data.metrics);
    } catch (error) {
        console.error('Failed to load model metrics:', error);
    }
}

async function makePrediction(inputData) {
    try {
        const data = await apiCall('/predict', {
            method: 'POST',
            body: JSON.stringify(inputData)
        });
        
        // Save to history
        savePredictionToHistory(data);
        
        return data;
    } catch (error) {
        console.error('Prediction failed:', error);
        throw error;
    }
}

async function makeBatchPrediction(batchData) {
    try {
        const data = await apiCall('/predict-batch', {
            method: 'POST',
            body: JSON.stringify({ data: batchData })
        });
        
        return data;
    } catch (error) {
        console.error('Batch prediction failed:', error);
        throw error;
    }
}

// ============================================
// Form Handling
// ============================================
async function handlePredictionSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const inputData = {};
    
    // Process form data
    for (let [key, value] of formData.entries()) {
        if (key === 'HasCrCard' || key === 'IsActiveMember') {
            inputData[key] = formData.get(key) ? 1 : 0;
        } else if (key === 'CreditScore' || key === 'Age' || key === 'Tenure' || key === 'NumOfProducts') {
            inputData[key] = parseInt(value);
        } else if (key === 'Balance' || key === 'EstimatedSalary') {
            inputData[key] = parseFloat(value);
        } else {
            inputData[key] = value;
        }
    }
    
    // Handle checkboxes separately
    inputData.HasCrCard = document.getElementById('hasCrCard').checked ? 1 : 0;
    inputData.IsActiveMember = document.getElementById('isActiveMember').checked ? 1 : 0;
    
    console.log('Sending prediction request:', inputData);
    
    try {
        // Show loading state
        showLoading();
        
        const result = await makePrediction(inputData);
        
        // Hide loading and show results
        hideLoading();
        renderPredictionResult(result, inputData);
        
    } catch (error) {
        hideLoading();
        showError('Error al realizar la predicción. Por favor, intenta nuevamente.');
    }
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('predictionResult').style.display = 'none';
}

function fillExampleData() {
    const example = testDataSamples[1].data; // Cliente Estándar
    
    document.getElementById('creditScore').value = example.CreditScore;
    document.getElementById('geography').value = example.Geography;
    document.getElementById('gender').value = example.Gender;
    document.getElementById('age').value = example.Age;
    document.getElementById('tenure').value = example.Tenure;
    document.getElementById('balance').value = example.Balance;
    document.getElementById('numProducts').value = example.NumOfProducts;
    document.getElementById('hasCrCard').checked = example.HasCrCard === 1;
    document.getElementById('isActiveMember').checked = example.IsActiveMember === 1;
    document.getElementById('estimatedSalary').value = example.EstimatedSalary;
}

function loadTestData(index) {
    const testData = testDataSamples[index];
    
    // Switch to individual prediction tab
    document.querySelector('.tab-btn[data-tab="individual"]').click();
    
    // Fill form with test data
    document.getElementById('creditScore').value = testData.data.CreditScore;
    document.getElementById('geography').value = testData.data.Geography;
    document.getElementById('gender').value = testData.data.Gender;
    document.getElementById('age').value = testData.data.Age;
    document.getElementById('tenure').value = testData.data.Tenure;
    document.getElementById('balance').value = testData.data.Balance;
    document.getElementById('numProducts').value = testData.data.NumOfProducts;
    document.getElementById('hasCrCard').checked = testData.data.HasCrCard === 1;
    document.getElementById('isActiveMember').checked = testData.data.IsActiveMember === 1;
    document.getElementById('estimatedSalary').value = testData.data.EstimatedSalary;
    
    // Scroll to form
    document.getElementById('predictionForm').scrollIntoView({ behavior: 'smooth' });
    
    // Show notification
    showNotification(`Datos cargados: ${testData.name}`, 'success');
}

// ============================================
// File Upload Handling
// ============================================
function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    if (!uploadArea || !fileInput) return;
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Por favor, selecciona un archivo CSV válido.');
        return;
    }
    
    try {
        showLoading();
        
        const text = await file.text();
        const data = parseCSV(text);
        
        console.log('Parsed CSV data:', data);
        
        const result = await makeBatchPrediction(data);
        
        hideLoading();
        renderBatchResults(result);
        
    } catch (error) {
        hideLoading();
        showError('Error al procesar el archivo CSV.');
        console.error(error);
    }
}

function parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    
    const data = [];
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim());
        const row = {};
        
        headers.forEach((header, index) => {
            const value = values[index];
            
            if (header === 'Geography' || header === 'Gender') {
                row[header] = value;
            } else if (header === 'HasCrCard' || header === 'IsActiveMember') {
                row[header] = parseInt(value);
            } else if (header === 'Balance' || header === 'EstimatedSalary') {
                row[header] = parseFloat(value);
            } else {
                row[header] = parseInt(value);
            }
        });
        
        data.push(row);
    }
    
    return data;
}

function downloadTemplate() {
    const template = `CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary
619,France,Female,42,2,0,1,1,1,101348.88
608,Spain,Female,41,1,83807.86,1,0,1,112542.58
502,France,Female,42,8,159660.8,3,1,0,113931.57`;
    
    const blob = new Blob([template], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'template.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('Plantilla descargada correctamente', 'success');
}

// ============================================
// Rendering Functions
// ============================================
function renderSystemStatus(data) {
    const container = document.getElementById('systemStatus');
    
    if (data.status === 'error') {
        container.innerHTML = `
            <div class="status-item">
                <span>Estado</span>
                <span class="status-badge" style="background: #fee2e2; color: #991b1b;">
                    Desconectado
                </span>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="status-item">
            <span>API</span>
            <span class="status-badge healthy">
                ${data.status === 'healthy' ? 'Saludable' : data.status}
            </span>
        </div>
        <div class="status-item">
            <span>Modelo</span>
            <span class="status-badge healthy">
                ${data.model_loaded ? 'Cargado' : 'No Cargado'}
            </span>
        </div>
        <div class="status-item">
            <span>Preprocesador</span>
            <span class="status-badge healthy">
                ${data.preprocessor_loaded ? 'Cargado' : 'No Cargado'}
            </span>
        </div>
    `;
}

function renderModelMetrics(metrics) {
    if (!metrics) return;
    
    const container = document.getElementById('modelMetrics');
    
    container.innerHTML = `
        <div class="metric-item">
            <span class="metric-label">Accuracy</span>
            <span class="metric-value">${(metrics.test_accuracy * 100).toFixed(2)}%</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">ROC-AUC</span>
            <span class="metric-value">${(metrics.test_roc_auc * 100).toFixed(2)}%</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">F1-Score</span>
            <span class="metric-value">${(metrics.test_f1 * 100).toFixed(2)}%</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">CV Media</span>
            <span class="metric-value">${(metrics.cv_mean * 100).toFixed(2)}%</span>
        </div>
    `;
}

function renderModelInfo(data) {
    const container = document.getElementById('modelInfoContent');
    
    container.innerHTML = `
        <div class="info-grid">
            <div class="info-card">
                <h4><i class="fas fa-robot"></i> Información del Modelo</h4>
                <p><strong>Nombre:</strong> ${data.model_name}</p>
                <p><strong>Tipo:</strong> ${data.model_type}</p>
                <p><strong>Características:</strong> ${data.n_features}</p>
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h5>Test Accuracy</h5>
                <div class="value">${(data.metrics.test_accuracy * 100).toFixed(2)}%</div>
            </div>
            <div class="metric-card">
                <h5>Test F1-Score</h5>
                <div class="value">${(data.metrics.test_f1 * 100).toFixed(2)}%</div>
            </div>
            <div class="metric-card">
                <h5>Test ROC-AUC</h5>
                <div class="value">${(data.metrics.test_roc_auc * 100).toFixed(2)}%</div>
            </div>
            <div class="metric-card">
                <h5>CV Mean Score</h5>
                <div class="value">${(data.metrics.cv_mean * 100).toFixed(2)}%</div>
            </div>
        </div>
        
        <div class="info-card">
            <h4><i class="fas fa-chart-line"></i> Características del Modelo</h4>
            <ul style="list-style: none; padding: 0;">
                <li style="padding: 0.5rem 0;"><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Gradient Boosting Classifier</li>
                <li style="padding: 0.5rem 0;"><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Entrenado con 11 características</li>
                <li style="padding: 0.5rem 0;"><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Cross-validation con 5 folds</li>
                <li style="padding: 0.5rem 0;"><i class="fas fa-check-circle" style="color: var(--success-color);"></i> Optimización de hiperparámetros</li>
            </ul>
        </div>
    `;
}

function renderPredictionResult(result, inputData) {
    const container = document.getElementById('predictionResult');
    const probability = result.churn_probability;
    const prediction = result.prediction === 1;
    
    const icon = prediction ? 'fa-user-times' : 'fa-user-check';
    const iconClass = prediction ? 'churn' : 'no-churn';
    const predictionText = prediction ? 'Predicción: CHURN' : 'Predicción: NO CHURN';
    const interpretationText = prediction 
        ? 'El cliente tiene alta probabilidad de abandonar el servicio.'
        : 'El cliente probablemente permanecerá con el servicio.';
    
    container.innerHTML = `
        <div class="result-header">
            <h3>Resultados de la Predicción</h3>
        </div>
        
        <div class="result-prediction">
            <div class="prediction-icon ${iconClass}">
                <i class="fas ${icon}"></i>
            </div>
            <div class="prediction-text">
                <h3>${predictionText}</h3>
                <div class="prediction-probability">${(probability * 100).toFixed(1)}%</div>
                <p>${interpretationText}</p>
            </div>
        </div>
        
        <div class="probability-bar">
            <div class="probability-fill" style="width: ${probability * 100}%">
                ${(probability * 100).toFixed(1)}%
            </div>
        </div>
        
        <div class="result-details">
            <div class="detail-card">
                <div class="detail-label">Credit Score</div>
                <div class="detail-value">${inputData.CreditScore}</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Edad</div>
                <div class="detail-value">${inputData.Age} años</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Antigüedad</div>
                <div class="detail-value">${inputData.Tenure} años</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Balance</div>
                <div class="detail-value">$${formatNumber(inputData.Balance)}</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Productos</div>
                <div class="detail-value">${inputData.NumOfProducts}</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Salario</div>
                <div class="detail-value">$${formatNumber(inputData.EstimatedSalary)}</div>
            </div>
        </div>
    `;
    
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderBatchResults(results) {
    const container = document.getElementById('batchResult');
    
    if (!results.predictions || results.predictions.length === 0) {
        container.innerHTML = '<p>No se obtuvieron resultados.</p>';
        container.style.display = 'block';
        return;
    }
    
    const churnCount = results.predictions.filter(p => p.prediction === 1).length;
    const noChurnCount = results.predictions.length - churnCount;
    const avgProbability = results.predictions.reduce((sum, p) => sum + p.churn_probability, 0) / results.predictions.length;
    
    let tableRows = '';
    results.predictions.forEach((pred, index) => {
        const prediction = pred.prediction === 1 ? 'CHURN' : 'NO CHURN';
        const predClass = pred.prediction === 1 ? 'danger-color' : 'success-color';
        const probability = (pred.churn_probability * 100).toFixed(1);
        
        tableRows += `
            <tr>
                <td>${index + 1}</td>
                <td style="color: var(--${predClass}); font-weight: 600;">${prediction}</td>
                <td>${probability}%</td>
                <td>
                    <div style="width: 100%; background: var(--bg-tertiary); border-radius: 4px; height: 8px;">
                        <div style="width: ${probability}%; background: linear-gradient(90deg, var(--success-color) 0%, var(--warning-color) 50%, var(--danger-color) 100%); height: 100%; border-radius: 4px;"></div>
                    </div>
                </td>
            </tr>
        `;
    });
    
    container.innerHTML = `
        <div class="result-header">
            <h3>Resultados de Predicción por Lote</h3>
            <p>Se procesaron ${results.predictions.length} registros</p>
        </div>
        
        <div class="result-details" style="margin-bottom: var(--spacing-lg);">
            <div class="detail-card">
                <div class="detail-label">Total Procesados</div>
                <div class="detail-value">${results.predictions.length}</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Predicción: CHURN</div>
                <div class="detail-value" style="color: var(--danger-color);">${churnCount}</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Predicción: NO CHURN</div>
                <div class="detail-value" style="color: var(--success-color);">${noChurnCount}</div>
            </div>
            <div class="detail-card">
                <div class="detail-label">Probabilidad Promedio</div>
                <div class="detail-value">${(avgProbability * 100).toFixed(1)}%</div>
            </div>
        </div>
        
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--bg-tertiary); border-bottom: 2px solid var(--border-color);">
                        <th style="padding: var(--spacing-sm); text-align: left;">#</th>
                        <th style="padding: var(--spacing-sm); text-align: left;">Predicción</th>
                        <th style="padding: var(--spacing-sm); text-align: left;">Probabilidad</th>
                        <th style="padding: var(--spacing-sm); text-align: left;">Visualización</th>
                    </tr>
                </thead>
                <tbody>
                    ${tableRows}
                </tbody>
            </table>
        </div>
        
        <div style="margin-top: var(--spacing-lg); text-align: center;">
            <button class="btn btn-primary" onclick="downloadBatchResults()">
                <i class="fas fa-download"></i> Descargar Resultados
            </button>
        </div>
    `;
    
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function downloadBatchResults() {
    // This would download the batch results as CSV
    showNotification('Funcionalidad de descarga en desarrollo', 'info');
}

// ============================================
// History Management
// ============================================
function savePredictionToHistory(result) {
    const historyItem = {
        timestamp: new Date().toISOString(),
        prediction: result.prediction,
        probability: result.churn_probability
    };
    
    state.predictions.unshift(historyItem);
    
    // Keep only last 10 predictions
    if (state.predictions.length > 10) {
        state.predictions = state.predictions.slice(0, 10);
    }
    
    renderHistory();
}

function renderHistory() {
    const container = document.getElementById('predictionHistory');
    
    if (state.predictions.length === 0) {
        container.innerHTML = '<p class="empty-state">No hay predicciones aún</p>';
        return;
    }
    
    let html = '';
    state.predictions.forEach((item, index) => {
        const date = new Date(item.timestamp);
        const time = date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
        const prediction = item.prediction === 1 ? 'CHURN' : 'NO CHURN';
        const predClass = item.prediction === 1 ? 'churn' : 'no-churn';
        const icon = item.prediction === 1 ? 'fa-user-times' : 'fa-user-check';
        
        html += `
            <div class="history-item">
                <div class="history-time">${time}</div>
                <div class="history-result ${predClass}">
                    <i class="fas ${icon}"></i>
                    ${prediction} - ${(item.probability * 100).toFixed(1)}%
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// ============================================
// UI Helpers
// ============================================
function showLoading() {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    overlay.innerHTML = `
        <div style="background: white; padding: 2rem; border-radius: 1rem; text-align: center;">
            <i class="fas fa-spinner fa-spin" style="font-size: 3rem; color: var(--primary-color);"></i>
            <p style="margin-top: 1rem; font-size: 1.125rem; font-weight: 600;">Procesando...</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        min-width: 300px;
        animation: slideIn 0.3s ease;
    `;
    
    const icons = {
        success: { icon: 'fa-check-circle', color: 'var(--success-color)' },
        error: { icon: 'fa-exclamation-circle', color: 'var(--danger-color)' },
        info: { icon: 'fa-info-circle', color: 'var(--primary-color)' }
    };
    
    const config = icons[type] || icons.info;
    
    notification.innerHTML = `
        <i class="fas ${config.icon}" style="font-size: 1.5rem; color: ${config.color};"></i>
        <span style="flex: 1;">${message}</span>
        <i class="fas fa-times" style="cursor: pointer; color: var(--text-light);" onclick="this.parentElement.remove()"></i>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ============================================
// Utility Functions
// ============================================
function formatNumber(num) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(num);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('MLOps Frontend loaded successfully');
