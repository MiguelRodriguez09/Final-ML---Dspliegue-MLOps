"""
Model Deployment API - MLOps Project

Este módulo implementa una API REST para servir el modelo de ML entrenado.
Utiliza Flask para exponer endpoints de predicción con soporte para batch.

Características principales:
- API REST con Flask
- Endpoint de predicción por lotes
- Validación de datos de entrada
- Logging de solicitudes
- Health check endpoint

Autor: MLOps Pipeline
Fecha: 2025
"""

import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

# Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelDeployment:
    """
    Clase para despliegue del modelo de ML como API.
    """
    
    def __init__(self, project_root: Path):
        """
        Inicializa el servicio de deployment.
        
        Parámetros:
        -----------
        project_root : Path
            Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.models_dir = self.project_root / 'mlops_pipeline' / 'models'
        self.logs_dir = self.project_root / 'mlops_pipeline' / 'logs'
        
        # Crear directorios
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.preprocessor = None
        self.metadata = None
        self.feature_names = None
        
        # Cargar modelo y preprocessor
        self._cargar_artefactos()
        
        logger.info("ModelDeployment inicializado correctamente")
    
    def _cargar_artefactos(self):
        """Carga el modelo, preprocessor y metadata."""
        try:
            # Cargar modelo
            model_path = self.models_dir / 'best_model.pkl'
            if not model_path.exists():
                raise FileNotFoundError(f"Modelo no encontrado en {model_path}")
            
            self.model = joblib.load(model_path)
            logger.info(f"✓ Modelo cargado desde: {model_path}")
            
            # Cargar preprocessor
            preprocessor_path = self.models_dir / 'preprocessor.pkl'
            if preprocessor_path.exists():
                self.preprocessor = joblib.load(preprocessor_path)
                logger.info(f"✓ Preprocessor cargado desde: {preprocessor_path}")
            else:
                logger.warning("⚠ Preprocessor no encontrado. Asegúrate de que los datos estén preprocesados.")
            
            # Cargar metadata
            metadata_path = self.models_dir / 'best_model_metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"✓ Metadata cargada: {self.metadata.get('nombre', 'N/A')}")
            
            # Cargar nombres de features
            feature_names_path = self.models_dir / 'feature_names.json'
            if feature_names_path.exists():
                with open(feature_names_path, 'r') as f:
                    self.feature_names = json.load(f)
                logger.info(f"✓ Nombres de features cargados: {len(self.feature_names)} features")
            
        except Exception as e:
            logger.error(f"✗ Error al cargar artefactos: {str(e)}")
            raise
    
    def validar_entrada(self, data: Dict) -> tuple:
        """
        Valida los datos de entrada.
        
        Parámetros:
        -----------
        data : dict
            Datos de entrada
            
        Retorna:
        --------
        tuple : (es_valido, mensaje_error)
        """
        if not data:
            return False, "No se proporcionaron datos"
        
        if 'instances' not in data and 'data' not in data:
            return False, "El JSON debe contener 'instances' o 'data'"
        
        instances = data.get('instances', data.get('data', []))
        
        if not isinstance(instances, list):
            return False, "'instances' o 'data' debe ser una lista"
        
        if len(instances) == 0:
            return False, "La lista de instancias está vacía"
        
        return True, None
    
    def preprocesar_entrada(self, instances: List[Dict]) -> np.ndarray:
        """
        Preprocesa las instancias de entrada.
        
        Parámetros:
        -----------
        instances : list
            Lista de diccionarios con los datos
            
        Retorna:
        --------
        np.ndarray : Datos preprocesados
        """
        # Convertir a DataFrame
        df = pd.DataFrame(instances)
        
        # Aplicar preprocessor si existe
        if self.preprocessor is not None:
            X = self.preprocessor.transform(df)
        else:
            X = df.values
        
        return X
    
    def predecir(self, X: np.ndarray, include_proba: bool = False) -> Dict:
        """
        Realiza predicciones con el modelo.
        
        Parámetros:
        -----------
        X : np.ndarray
            Datos preprocesados
        include_proba : bool
            Si True, incluye probabilidades en la respuesta
            
        Retorna:
        --------
        dict : Diccionario con predicciones
        """
        # Predicciones
        predicciones = self.model.predict(X)
        
        resultado = {
            'predictions': predicciones.tolist()
        }
        
        # Agregar probabilidades si se solicita y el modelo lo soporta
        if include_proba:
            try:
                probabilidades = self.model.predict_proba(X)
                resultado['probabilities'] = probabilidades.tolist()
            except AttributeError:
                logger.warning("El modelo no soporta predict_proba")
        
        return resultado
    
    def procesar_solicitud(self, data: Dict) -> Dict:
        """
        Procesa una solicitud completa de predicción.
        
        Parámetros:
        -----------
        data : dict
            Datos de la solicitud
            
        Retorna:
        --------
        dict : Respuesta con predicciones o error
        """
        inicio = datetime.now()
        
        try:
            # Validar entrada
            es_valido, mensaje_error = self.validar_entrada(data)
            if not es_valido:
                return {
                    'error': mensaje_error,
                    'status': 'failed'
                }
            
            # Obtener instancias
            instances = data.get('instances', data.get('data', []))
            include_proba = data.get('include_probabilities', False)
            
            # Preprocesar
            X = self.preprocesar_entrada(instances)
            
            # Predecir
            resultado = self.predecir(X, include_proba=include_proba)
            
            # Agregar metadata
            tiempo_procesamiento = (datetime.now() - inicio).total_seconds()
            resultado['metadata'] = {
                'n_instances': len(instances),
                'processing_time_seconds': tiempo_procesamiento,
                'model_name': self.metadata.get('nombre', 'Unknown') if self.metadata else 'Unknown',
                'timestamp': datetime.now().isoformat()
            }
            resultado['status'] = 'success'
            
            logger.info(f"Predicción exitosa: {len(instances)} instancias en {tiempo_procesamiento:.3f}s")
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en predicción: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def obtener_info_modelo(self) -> Dict:
        """
        Retorna información sobre el modelo desplegado.
        
        Retorna:
        --------
        dict : Información del modelo
        """
        info = {
            'model_loaded': self.model is not None,
            'preprocessor_loaded': self.preprocessor is not None,
            'status': 'ready' if self.model is not None else 'not_ready'
        }
        
        if self.metadata:
            info['model_info'] = self.metadata
        
        if self.feature_names:
            info['n_features'] = len(self.feature_names)
            info['feature_names'] = self.feature_names[:10]  # Primeras 10
        
        return info


# Crear aplicación Flask
def crear_app(project_root: Path = None) -> Flask:
    """
    Crea y configura la aplicación Flask.
    
    Parámetros:
    -----------
    project_root : Path, opcional
        Ruta raíz del proyecto
        
    Retorna:
    --------
    Flask : Aplicación configurada
    """
    if project_root is None:
        project_root = Path(__file__).parent.parent.parent
    
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS
    
    # Inicializar deployment
    deployment = ModelDeployment(project_root)
    
    @app.route('/', methods=['GET'])
    def home():
        """Endpoint raíz."""
        return jsonify({
            'message': 'MLOps Model Deployment API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'info': '/info',
                'predict': '/predict (POST)'
            }
        })
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_loaded': deployment.model is not None
        })
    
    @app.route('/info', methods=['GET'])
    def info():
        """Información del modelo."""
        return jsonify(deployment.obtener_info_modelo())
    
    @app.route('/predict', methods=['POST'])
    def predict():
        """
        Endpoint de predicción.
        
        Espera un JSON con el siguiente formato:
        {
            "instances": [
                {"feature1": value1, "feature2": value2, ...},
                {"feature1": value1, "feature2": value2, ...}
            ],
            "include_probabilities": false  // opcional
        }
        
        O alternativamente:
        {
            "data": [
                {"feature1": value1, "feature2": value2, ...}
            ]
        }
        """
        try:
            data = request.get_json()
            
            if data is None:
                return jsonify({
                    'error': 'No se proporcionó JSON en la solicitud',
                    'status': 'failed'
                }), 400
            
            resultado = deployment.procesar_solicitud(data)
            
            if resultado['status'] == 'failed':
                return jsonify(resultado), 400
            
            return jsonify(resultado), 200
            
        except Exception as e:
            logger.error(f"Error en endpoint /predict: {str(e)}")
            return jsonify({
                'error': str(e),
                'status': 'failed'
            }), 500
    
    return app


def main():
    """
    Función principal para ejecutar el servidor.
    """
    print("="*80)
    print("MODEL DEPLOYMENT API")
    print("="*80)
    
    # Configuración
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # Crear aplicación
    project_root = Path(__file__).parent.parent.parent
    app = crear_app(project_root)
    
    print(f"\n✓ Servidor iniciado en http://{HOST}:{PORT}")
    print(f"\nEndpoints disponibles:")
    print(f"  - GET  /          : Información general")
    print(f"  - GET  /health    : Health check")
    print(f"  - GET  /info      : Información del modelo")
    print(f"  - POST /predict   : Realizar predicciones")
    print(f"\nEjemplo de uso:")
    print(f"  curl -X POST http://localhost:{PORT}/predict \\")
    print(f"    -H 'Content-Type: application/json' \\")
    print(f"    -d '{{\"instances\": [{{\"feature1\": 1, \"feature2\": 2}}]}}'")
    print("\n" + "="*80)
    
    # Ejecutar servidor
    app.run(host=HOST, port=PORT, debug=DEBUG)


if __name__ == "__main__":
    main()
