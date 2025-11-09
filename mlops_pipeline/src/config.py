"""
Configuración y constantes del proyecto MLOps.

Este módulo centraliza todas las configuraciones, constantes y valores
por defecto utilizados en el proyecto.

Autor: MLOps Pipeline
Fecha: 2025
"""

from pathlib import Path
from typing import Dict, Any

# ============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'mlops_pipeline' / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
MODELS_DIR = PROJECT_ROOT / 'mlops_pipeline' / 'models'
REPORTS_DIR = PROJECT_ROOT / 'mlops_pipeline' / 'reports'
MONITORING_DIR = PROJECT_ROOT / 'mlops_pipeline' / 'monitoring'
LOGS_DIR = PROJECT_ROOT / 'mlops_pipeline' / 'logs'

# ============================================================================
# CONSTANTES DE FEATURE ENGINEERING
# ============================================================================

RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# Estrategias de imputación
IMPUTATION_STRATEGIES = {
    'numeric': 'median',
    'categorical': 'most_frequent'
}

# Estrategias de escalado
SCALING_STRATEGIES = {
    'standard': 'StandardScaler',
    'minmax': 'MinMaxScaler',
    'robust': 'RobustScaler'
}

# ============================================================================
# CONSTANTES DE ENTRENAMIENTO
# ============================================================================

# Modelos disponibles
CLASSIFICATION_MODELS = [
    'Logistic Regression',
    'Decision Tree',
    'Random Forest',
    'Gradient Boosting',
    'SVM',
    'K-Nearest Neighbors',
    'Naive Bayes',
    'XGBoost',
    'LightGBM'
]

# Hiperparámetros por defecto
DEFAULT_HYPERPARAMETERS: Dict[str, Dict[str, Any]] = {
    'Logistic Regression': {
        'max_iter': 1000,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'Decision Tree': {
        'max_depth': 10,
        'random_state': RANDOM_STATE
    },
    'Random Forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'Gradient Boosting': {
        'n_estimators': 100,
        'max_depth': 5,
        'random_state': RANDOM_STATE
    },
    'SVM': {
        'kernel': 'rbf',
        'probability': True,
        'random_state': RANDOM_STATE
    },
    'K-Nearest Neighbors': {
        'n_neighbors': 5,
        'n_jobs': -1
    },
    'XGBoost': {
        'n_estimators': 100,
        'max_depth': 5,
        'random_state': RANDOM_STATE,
        'eval_metric': 'logloss',
        'use_label_encoder': False
    },
    'LightGBM': {
        'n_estimators': 100,
        'max_depth': 5,
        'random_state': RANDOM_STATE,
        'verbose': -1
    }
}

# Métricas de evaluación
CLASSIFICATION_METRICS = [
    'accuracy',
    'precision',
    'recall',
    'f1',
    'roc_auc'
]

# ============================================================================
# CONSTANTES DE MONITOREO
# ============================================================================

# Umbrales de drift
DRIFT_THRESHOLDS = {
    'ks_statistic': 0.1,
    'psi': 0.2,
    'jensen_shannon': 0.1,
    'chi_square_pvalue': 0.05
}

# Configuración de histogramas
HISTOGRAM_BINS = 10

# Niveles de severidad
SEVERITY_LEVELS = {
    'low': 'baja',
    'medium': 'media',
    'high': 'alta',
    'critical': 'critica'
}

# ============================================================================
# CONSTANTES DE API
# ============================================================================

# Configuración de Flask
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# Límites de API
API_LIMITS = {
    'max_batch_size': 1000,
    'request_timeout': 30
}

# ============================================================================
# CONSTANTES DE LOGGING
# ============================================================================

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# ============================================================================
# CONSTANTES DE VISUALIZACIÓN
# ============================================================================

# Estilo de plots
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
FIGURE_SIZE = (12, 8)
DPI = 100

# Paleta de colores
COLOR_PALETTE = 'viridis'

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def crear_directorios() -> None:
    """Crea todos los directorios necesarios del proyecto."""
    directorios = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        MODELS_DIR,
        REPORTS_DIR,
        MONITORING_DIR,
        LOGS_DIR
    ]
    
    for directorio in directorios:
        directorio.mkdir(parents=True, exist_ok=True)


def obtener_configuracion() -> Dict[str, Any]:
    """
    Retorna un diccionario con toda la configuración del proyecto.
    
    Returns:
        Dict[str, Any]: Configuración completa del proyecto
    """
    return {
        'directorios': {
            'project_root': str(PROJECT_ROOT),
            'data': str(DATA_DIR),
            'models': str(MODELS_DIR),
            'reports': str(REPORTS_DIR),
            'monitoring': str(MONITORING_DIR),
            'logs': str(LOGS_DIR)
        },
        'feature_engineering': {
            'random_state': RANDOM_STATE,
            'test_size': TEST_SIZE,
            'validation_size': VALIDATION_SIZE
        },
        'training': {
            'models': CLASSIFICATION_MODELS,
            'metrics': CLASSIFICATION_METRICS
        },
        'monitoring': {
            'thresholds': DRIFT_THRESHOLDS,
            'histogram_bins': HISTOGRAM_BINS
        },
        'api': {
            'flask': FLASK_CONFIG,
            'limits': API_LIMITS
        }
    }
