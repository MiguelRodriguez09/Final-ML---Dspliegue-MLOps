"""
Model Deployment Module para MLOps Pipeline.

Este módulo implementa una API REST usando Flask para servir
predicciones del modelo entrenado.

Endpoints:
    - GET /: Health check
    - POST /predict: Predicción individual o por lotes
    - GET /model-info: Información del modelo
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Union

import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Variables globales
MODEL = None
PREPROCESSOR = None
FEATURE_NAMES = None
MODEL_METADATA = None
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_artifacts() -> None:
    """
    Carga el modelo entrenado, preprocessor y metadatos.
    """
    global MODEL, PREPROCESSOR, FEATURE_NAMES, MODEL_METADATA
    
    try:
        # Cargar modelo
        model_path = PROJECT_ROOT / 'best_model.pkl'
        MODEL = joblib.load(model_path)
        logger.info(f"Modelo cargado desde: {model_path}")
        
        # Cargar preprocessor
        preprocessor_path = PROJECT_ROOT / 'preprocessor.pkl'
        PREPROCESSOR = joblib.load(preprocessor_path)
        logger.info(f"Preprocessor cargado desde: {preprocessor_path}")
        
        # Cargar metadatos del modelo
        metadata_path = PROJECT_ROOT / 'model_metadata.json'
        with open(metadata_path, 'r', encoding='utf-8') as f:
            MODEL_METADATA = json.load(f)
        logger.info("Metadatos del modelo cargados")
        
        # Cargar nombres de features
        fe_metadata_path = PROJECT_ROOT / 'feature_engineering_metadata.json'
        with open(fe_metadata_path, 'r', encoding='utf-8') as f:
            fe_metadata = json.load(f)
            FEATURE_NAMES = fe_metadata.get('feature_names', [])
        logger.info(f"Nombres de features cargados: {len(FEATURE_NAMES)} features")
        
    except FileNotFoundError as e:
        logger.error(f"Error al cargar artefactos: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al cargar artefactos: {e}")
        raise


def validate_input_data(data: Union[Dict, List[Dict]]) -> pd.DataFrame:
    """
    Valida y convierte los datos de entrada a DataFrame.
    
    Args:
        data: Datos de entrada (dict o lista de dicts)
    
    Returns:
        DataFrame validado
    
    Raises:
        ValueError: Si los datos son inválidos
    """
    # Convertir a lista si es un solo registro
    if isinstance(data, dict):
        data = [data]
    
    # Crear DataFrame
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        raise ValueError(f"No se pudo crear DataFrame desde los datos: {e}")
    
    # Validar que existan las columnas necesarias
    # (El preprocessor manejará las transformaciones necesarias)
    
    logger.info(f"Datos validados: {len(df)} registros")
    return df


def preprocess_data(df: pd.DataFrame) -> np.ndarray:
    """
    Preprocesa los datos usando el pipeline guardado.
    
    Args:
        df: DataFrame con datos de entrada
    
    Returns:
        Array numpy con datos transformados
    """
    try:
        X_transformed = PREPROCESSOR.transform(df)
        logger.info(f"Datos preprocesados: shape {X_transformed.shape}")
        return X_transformed
    except Exception as e:
        logger.error(f"Error en preprocesamiento: {e}")
        raise ValueError(f"Error al preprocesar datos: {e}")


def make_predictions(X: np.ndarray) -> Dict[str, Any]:
    """
    Genera predicciones usando el modelo cargado.
    
    Args:
        X: Array con features preprocesadas
    
    Returns:
        Diccionario con predicciones y probabilidades
    """
    try:
        # Predicciones
        predictions = MODEL.predict(X)
        
        # Probabilidades (si el modelo lo soporta)
        probabilities = None
        if hasattr(MODEL, 'predict_proba'):
            probabilities = MODEL.predict_proba(X)
        
        result = {
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist() if probabilities is not None else None,
            'n_samples': len(predictions)
        }
        
        logger.info(f"Predicciones generadas: {len(predictions)} muestras")
        return result
        
    except Exception as e:
        logger.error(f"Error al generar predicciones: {e}")
        raise ValueError(f"Error en predicción: {e}")


@app.route('/', methods=['GET'])
def health_check() -> tuple:
    """
    Endpoint de health check.
    
    Returns:
        JSON con estado del servicio
    """
    status = {
        'status': 'healthy',
        'service': 'MLOps Model API',
        'model_loaded': MODEL is not None,
        'preprocessor_loaded': PREPROCESSOR is not None
    }
    return jsonify(status), 200


@app.route('/model-info', methods=['GET'])
def model_info() -> tuple:
    """
    Endpoint para obtener información del modelo.
    
    Returns:
        JSON con información del modelo
    """
    if MODEL_METADATA is None:
        return jsonify({'error': 'Metadatos del modelo no disponibles'}), 500
    
    info = {
        'model_name': MODEL_METADATA.get('model_name', 'Unknown'),
        'model_type': MODEL_METADATA.get('model_type', 'Unknown'),
        'metrics': MODEL_METADATA.get('metrics', {}),
        'n_features': len(FEATURE_NAMES) if FEATURE_NAMES else 0
    }
    
    return jsonify(info), 200


@app.route('/predict', methods=['POST'])
def predict() -> tuple:
    """
    Endpoint para realizar predicciones.
    
    Request Body:
        JSON: Objeto o array de objetos con features
        CSV: Archivo CSV con registros
    
    Returns:
        JSON con predicciones
    """
    try:
        # Verificar que el modelo esté cargado
        if MODEL is None or PREPROCESSOR is None:
            return jsonify({'error': 'Modelo no cargado'}), 500
        
        # Obtener datos del request
        if request.is_json:
            # Entrada JSON
            data = request.get_json()
            df = validate_input_data(data)
            
        elif 'file' in request.files:
            # Entrada CSV
            file = request.files['file']
            try:
                df = pd.read_csv(file)
                logger.info(f"CSV cargado: {len(df)} registros")
            except Exception as e:
                return jsonify({'error': f'Error al leer CSV: {e}'}), 400
        else:
            return jsonify({'error': 'Formato no soportado. Use JSON o CSV'}), 400
        
        # Preprocesar datos
        X_transformed = preprocess_data(df)
        
        # Generar predicciones
        predictions_result = make_predictions(X_transformed)
        
        # Agregar información adicional
        response = {
            'success': True,
            'predictions': predictions_result['predictions'],
            'probabilities': predictions_result['probabilities'],
            'n_samples': predictions_result['n_samples'],
            'model': MODEL_METADATA.get('model_name', 'Unknown')
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@app.route('/predict-batch', methods=['POST'])
def predict_batch() -> tuple:
    """
    Endpoint optimizado para predicciones por lotes grandes.
    
    Request Body:
        JSON array con múltiples registros
    
    Returns:
        JSON con predicciones
    """
    try:
        # Verificar que el modelo esté cargado
        if MODEL is None or PREPROCESSOR is None:
            return jsonify({'error': 'Modelo no cargado'}), 500
        
        # Obtener datos
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Se esperaba un array de objetos'}), 400
        
        # Validar y convertir
        df = validate_input_data(data)
        
        # Preprocesar
        X_transformed = preprocess_data(df)
        
        # Predicciones
        predictions_result = make_predictions(X_transformed)
        
        # Crear respuesta detallada por registro
        detailed_predictions = []
        for idx, (pred, prob) in enumerate(zip(
            predictions_result['predictions'],
            predictions_result['probabilities'] if predictions_result['probabilities'] else [None] * len(predictions_result['predictions'])
        )):
            record = {
                'index': idx,
                'prediction': int(pred),
                'probability': prob if prob is not None else None
            }
            detailed_predictions.append(record)
        
        response = {
            'success': True,
            'n_samples': len(detailed_predictions),
            'predictions': detailed_predictions,
            'model': MODEL_METADATA.get('model_name', 'Unknown')
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


def main() -> None:
    """
    Función principal para iniciar el servidor Flask.
    """
    print("="*70)
    print("MODEL DEPLOYMENT API - MLOps Pipeline")
    print("="*70)
    
    # Cargar artefactos
    print("\n[1/2] Cargando artefactos del modelo...")
    load_artifacts()
    print("✓ Artefactos cargados")
    
    # Información del modelo
    print("\n[2/2] Información del modelo:")
    print(f"  Modelo: {MODEL_METADATA.get('model_name', 'Unknown')}")
    print(f"  Tipo: {MODEL_METADATA.get('model_type', 'Unknown')}")
    print(f"  Features: {len(FEATURE_NAMES) if FEATURE_NAMES else 0}")
    
    print("\n" + "="*70)
    print("SERVIDOR LISTO")
    print("="*70)
    print("\nEndpoints disponibles:")
    print("  GET  /              - Health check")
    print("  GET  /model-info    - Información del modelo")
    print("  POST /predict       - Predicción (JSON o CSV)")
    print("  POST /predict-batch - Predicción por lotes")
    print("\n" + "="*70)
    
    # Iniciar servidor
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == "__main__":
    main()
