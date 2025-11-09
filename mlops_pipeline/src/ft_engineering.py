"""
Feature Engineering Pipeline - MLOps Project

Este módulo implementa un pipeline genérico y reutilizable de ingeniería de características
utilizando sklearn.pipeline.Pipeline y ColumnTransformer.

Características principales:
- Imputación de valores faltantes
- Escalado de características numéricas
- Codificación de características categóricas
- División de datos en conjuntos de entrenamiento y prueba
- Guardado y carga de transformadores

Autor: MLOps Pipeline
Fecha: 2025
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

# Scikit-learn imports
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer, KNNImputer
import joblib


class FeatureEngineeringPipeline:
    """
    Pipeline genérico de ingeniería de características para cualquier dataset tabular.
    """
    
    def __init__(self, project_root: Path):
        """
        Inicializa el pipeline de feature engineering.
        
        Parámetros:
        -----------
        project_root : Path
            Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / 'mlops_pipeline' / 'data'
        self.processed_dir = self.data_dir / 'processed'
        self.models_dir = self.project_root / 'mlops_pipeline' / 'models'
        
        # Crear directorios si no existen
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.preprocessor = None
        self.feature_names = None
        
    def cargar_datos(self, archivo: str = 'df_after_eda.pkl') -> pd.DataFrame:
        """
        Carga los datos procesados del EDA.
        
        Parámetros:
        -----------
        archivo : str
            Nombre del archivo a cargar
            
        Retorna:
        --------
        pd.DataFrame : DataFrame cargado
        """
        ruta = self.processed_dir / archivo
        
        if not ruta.exists():
            raise FileNotFoundError(f"El archivo {ruta} no existe")
        
        with open(ruta, 'rb') as f:
            df = pickle.load(f)
        
        print(f"✓ Datos cargados desde: {ruta}")
        print(f"  Shape: {df.shape}")
        
        return df
    
    def identificar_columnas(self, df: pd.DataFrame, 
                            target_col: str,
                            cols_ignorar: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Identifica automáticamente columnas numéricas y categóricas.
        
        Parámetros:
        -----------
        df : pd.DataFrame
            DataFrame a analizar
        target_col : str
            Nombre de la columna objetivo
        cols_ignorar : list, opcional
            Columnas a ignorar (ej: IDs)
            
        Retorna:
        --------
        dict : Diccionario con listas de columnas numéricas y categóricas
        """
        if cols_ignorar is None:
            cols_ignorar = []
        
        # Columnas a procesar (excluir target y columnas a ignorar)
        columnas_disponibles = [col for col in df.columns 
                               if col != target_col and col not in cols_ignorar]
        
        # Identificar columnas numéricas
        cols_numericas = df[columnas_disponibles].select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()
        
        # Identificar columnas categóricas
        cols_categoricas = df[columnas_disponibles].select_dtypes(
            include=['object', 'category']
        ).columns.tolist()
        
        print("\n" + "="*80)
        print("IDENTIFICACIÓN DE COLUMNAS")
        print("="*80)
        print(f"\nColumnas numéricas ({len(cols_numericas)}): {cols_numericas}")
        print(f"Columnas categóricas ({len(cols_categoricas)}): {cols_categoricas}")
        print(f"Columna objetivo: {target_col}")
        print(f"Columnas ignoradas: {cols_ignorar}")
        
        return {
            'numericas': cols_numericas,
            'categoricas': cols_categoricas,
            'target': target_col,
            'ignoradas': cols_ignorar
        }
    
    def crear_preprocessor(self, 
                          cols_numericas: List[str],
                          cols_categoricas: List[str],
                          numeric_strategy: str = 'median',
                          categorical_strategy: str = 'most_frequent',
                          scaler_type: str = 'standard',
                          encoder_type: str = 'onehot') -> ColumnTransformer:
        """
        Crea un preprocessor genérico usando ColumnTransformer.
        
        Parámetros:
        -----------
        cols_numericas : list
            Lista de columnas numéricas
        cols_categoricas : list
            Lista de columnas categóricas
        numeric_strategy : str
            Estrategia de imputación para valores numéricos
            ('mean', 'median', 'most_frequent', 'constant')
        categorical_strategy : str
            Estrategia de imputación para valores categóricos
            ('most_frequent', 'constant')
        scaler_type : str
            Tipo de escalador ('standard', 'minmax', 'robust')
        encoder_type : str
            Tipo de codificador ('onehot', 'ordinal', 'label')
            
        Retorna:
        --------
        ColumnTransformer : Preprocessor configurado
        """
        # Pipeline para variables numéricas
        numeric_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy=numeric_strategy)),
            ('scaler', self._get_scaler(scaler_type))
        ])
        
        # Pipeline para variables categóricas
        categorical_pipeline = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy=categorical_strategy, fill_value='missing')),
            ('encoder', self._get_encoder(encoder_type))
        ])
        
        # Combinar pipelines
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_pipeline, cols_numericas),
                ('cat', categorical_pipeline, cols_categoricas)
            ],
            remainder='drop'  # Eliminar columnas no especificadas
        )
        
        print("\n" + "="*80)
        print("PREPROCESSOR CREADO")
        print("="*80)
        print(f"\nPipeline Numérico:")
        print(f"  - Imputación: {numeric_strategy}")
        print(f"  - Escalado: {scaler_type}")
        print(f"\nPipeline Categórico:")
        print(f"  - Imputación: {categorical_strategy}")
        print(f"  - Codificación: {encoder_type}")
        
        self.preprocessor = preprocessor
        return preprocessor
    
    def _get_scaler(self, scaler_type: str):
        """Retorna el escalador según el tipo especificado."""
        scalers = {
            'standard': StandardScaler(),
            'minmax': MinMaxScaler(),
            'robust': RobustScaler()
        }
        return scalers.get(scaler_type.lower(), StandardScaler())
    
    def _get_encoder(self, encoder_type: str):
        """Retorna el codificador según el tipo especificado."""
        encoders = {
            'onehot': OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'),
            'ordinal': OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1),
        }
        return encoders.get(encoder_type.lower(), OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    
    def dividir_datos(self, 
                     df: pd.DataFrame,
                     target_col: str,
                     test_size: float = 0.2,
                     validation_size: float = 0.1,
                     random_state: int = 42,
                     stratify: bool = True) -> Tuple:
        """
        Divide los datos en conjuntos de entrenamiento, validación y prueba.
        
        Parámetros:
        -----------
        df : pd.DataFrame
            DataFrame completo
        target_col : str
            Nombre de la columna objetivo
        test_size : float
            Proporción del conjunto de prueba
        validation_size : float
            Proporción del conjunto de validación
        random_state : int
            Semilla para reproducibilidad
        stratify : bool
            Si True, realiza división estratificada
            
        Retorna:
        --------
        tuple : (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        stratify_param = y if stratify and len(y.unique()) <= 20 else None
        
        # Primera división: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state,
            stratify=stratify_param
        )
        
        # Segunda división: train vs val
        if validation_size > 0:
            val_size_adjusted = validation_size / (1 - test_size)
            stratify_param_val = y_temp if stratify and len(y_temp.unique()) <= 20 else None
            
            X_train, X_val, y_train, y_val = train_test_split(
                X_temp, y_temp,
                test_size=val_size_adjusted,
                random_state=random_state,
                stratify=stratify_param_val
            )
        else:
            X_train, y_train = X_temp, y_temp
            X_val, y_val = None, None
        
        print("\n" + "="*80)
        print("DIVISIÓN DE DATOS")
        print("="*80)
        print(f"\nConjunto de entrenamiento: {X_train.shape}")
        if X_val is not None:
            print(f"Conjunto de validación: {X_val.shape}")
        print(f"Conjunto de prueba: {X_test.shape}")
        print(f"\nDistribución de la variable objetivo:")
        print(f"  Train: {y_train.value_counts().to_dict()}")
        if y_val is not None:
            print(f"  Val: {y_val.value_counts().to_dict()}")
        print(f"  Test: {y_test.value_counts().to_dict()}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def ajustar_y_transformar(self,
                             X_train: pd.DataFrame,
                             X_val: Optional[pd.DataFrame] = None,
                             X_test: Optional[pd.DataFrame] = None) -> Tuple:
        """
        Ajusta el preprocessor con los datos de entrenamiento y transforma todos los conjuntos.
        
        Parámetros:
        -----------
        X_train : pd.DataFrame
            Conjunto de entrenamiento
        X_val : pd.DataFrame, opcional
            Conjunto de validación
        X_test : pd.DataFrame, opcional
            Conjunto de prueba
            
        Retorna:
        --------
        tuple : (X_train_transformed, X_val_transformed, X_test_transformed)
        """
        if self.preprocessor is None:
            raise ValueError("El preprocessor no ha sido creado. Ejecuta crear_preprocessor() primero.")
        
        print("\n" + "="*80)
        print("AJUSTANDO Y TRANSFORMANDO DATOS")
        print("="*80)
        
        # Ajustar y transformar entrenamiento
        print("\n1. Ajustando preprocessor con datos de entrenamiento...")
        X_train_transformed = self.preprocessor.fit_transform(X_train)
        print(f"   ✓ Train transformado: {X_train_transformed.shape}")
        
        # Transformar validación
        X_val_transformed = None
        if X_val is not None:
            print("\n2. Transformando conjunto de validación...")
            X_val_transformed = self.preprocessor.transform(X_val)
            print(f"   ✓ Validation transformado: {X_val_transformed.shape}")
        
        # Transformar test
        X_test_transformed = None
        if X_test is not None:
            print("\n3. Transformando conjunto de prueba...")
            X_test_transformed = self.preprocessor.transform(X_test)
            print(f"   ✓ Test transformado: {X_test_transformed.shape}")
        
        # Obtener nombres de características
        self._extraer_nombres_features(X_train)
        
        return X_train_transformed, X_val_transformed, X_test_transformed
    
    def _extraer_nombres_features(self, X_original: pd.DataFrame):
        """Extrae los nombres de las características después de la transformación."""
        try:
            feature_names = []
            
            for name, transformer, columns in self.preprocessor.transformers_:
                if name == 'remainder':
                    continue
                
                if hasattr(transformer, 'get_feature_names_out'):
                    names = transformer.get_feature_names_out(columns)
                    feature_names.extend(names)
                else:
                    feature_names.extend(columns)
            
            self.feature_names = feature_names
            print(f"\n✓ Nombres de características extraídos: {len(feature_names)} features")
            
        except Exception as e:
            print(f"⚠ No se pudieron extraer nombres de características: {str(e)}")
            self.feature_names = None
    
    def guardar_preprocessor(self, nombre_archivo: str = 'preprocessor.pkl'):
        """
        Guarda el preprocessor ajustado.
        
        Parámetros:
        -----------
        nombre_archivo : str
            Nombre del archivo de salida
        """
        if self.preprocessor is None:
            raise ValueError("No hay preprocessor para guardar")
        
        ruta = self.models_dir / nombre_archivo
        joblib.dump(self.preprocessor, ruta)
        
        # Guardar nombres de características si existen
        if self.feature_names is not None:
            ruta_features = self.models_dir / 'feature_names.json'
            with open(ruta_features, 'w') as f:
                json.dump(self.feature_names, f, indent=2)
        
        print(f"\n✓ Preprocessor guardado en: {ruta}")
        if self.feature_names is not None:
            print(f"✓ Nombres de características guardados en: {ruta_features}")
    
    def cargar_preprocessor(self, nombre_archivo: str = 'preprocessor.pkl'):
        """
        Carga un preprocessor previamente guardado.
        
        Parámetros:
        -----------
        nombre_archivo : str
            Nombre del archivo a cargar
        """
        ruta = self.models_dir / nombre_archivo
        
        if not ruta.exists():
            raise FileNotFoundError(f"El archivo {ruta} no existe")
        
        self.preprocessor = joblib.load(ruta)
        
        # Cargar nombres de características si existen
        ruta_features = self.models_dir / 'feature_names.json'
        if ruta_features.exists():
            with open(ruta_features, 'r') as f:
                self.feature_names = json.load(f)
        
        print(f"✓ Preprocessor cargado desde: {ruta}")
        if self.feature_names is not None:
            print(f"✓ Nombres de características cargados: {len(self.feature_names)} features")
    
    def guardar_datasets(self,
                        X_train, X_val, X_test,
                        y_train, y_val, y_test):
        """
        Guarda los conjuntos de datos procesados.
        
        Parámetros:
        -----------
        X_train, X_val, X_test : arrays
            Conjuntos de características
        y_train, y_val, y_test : arrays
            Conjuntos de etiquetas
        """
        datasets = {
            'X_train': X_train,
            'y_train': y_train,
            'X_test': X_test,
            'y_test': y_test
        }
        
        if X_val is not None:
            datasets['X_val'] = X_val
            datasets['y_val'] = y_val
        
        ruta = self.processed_dir / 'datasets_procesados.pkl'
        with open(ruta, 'wb') as f:
            pickle.dump(datasets, f)
        
        print(f"\n✓ Datasets guardados en: {ruta}")
        print(f"  Contenido: {list(datasets.keys())}")


def main():
    """
    Función principal para ejecutar el pipeline de feature engineering.
    """
    # Configuración
    project_root = Path(__file__).parent.parent.parent
    
    # Inicializar pipeline
    print("="*80)
    print("FEATURE ENGINEERING PIPELINE")
    print("="*80)
    
    fe_pipeline = FeatureEngineeringPipeline(project_root)
    
    # 1. Cargar datos
    print("\n[1/6] Cargando datos...")
    df = fe_pipeline.cargar_datos('df_after_eda.pkl')
    
    # 2. Identificar columnas (ajustar según el dataset)
    print("\n[2/6] Identificando columnas...")
    # Para Churn_Modelling.csv
    target_col = 'Exited' if 'Exited' in df.columns else df.columns[-1]
    cols_ignorar = ['RowNumber', 'CustomerId', 'Surname'] if 'RowNumber' in df.columns else []
    
    columnas = fe_pipeline.identificar_columnas(df, target_col, cols_ignorar)
    
    # 3. Dividir datos
    print("\n[3/6] Dividiendo datos...")
    # Eliminar columnas a ignorar antes de dividir
    df_procesado = df.drop(columns=cols_ignorar, errors='ignore')
    
    X_train, X_val, X_test, y_train, y_val, y_test = fe_pipeline.dividir_datos(
        df_procesado,
        target_col=target_col,
        test_size=0.2,
        validation_size=0.1,
        random_state=42,
        stratify=True
    )
    
    # 4. Crear preprocessor
    print("\n[4/6] Creando preprocessor...")
    preprocessor = fe_pipeline.crear_preprocessor(
        cols_numericas=columnas['numericas'],
        cols_categoricas=columnas['categoricas'],
        numeric_strategy='median',
        categorical_strategy='most_frequent',
        scaler_type='standard',
        encoder_type='onehot'
    )
    
    # 5. Ajustar y transformar
    print("\n[5/6] Ajustando y transformando datos...")
    X_train_t, X_val_t, X_test_t = fe_pipeline.ajustar_y_transformar(
        X_train, X_val, X_test
    )
    
    # 6. Guardar todo
    print("\n[6/6] Guardando resultados...")
    fe_pipeline.guardar_preprocessor('preprocessor.pkl')
    fe_pipeline.guardar_datasets(
        X_train_t, X_val_t, X_test_t,
        y_train, y_val, y_test
    )
    
    print("\n" + "="*80)
    print("✓ FEATURE ENGINEERING COMPLETADO")
    print("="*80)
    print("\nResumen:")
    print(f"  - Features transformadas: {X_train_t.shape[1]}")
    print(f"  - Train samples: {X_train_t.shape[0]}")
    if X_val_t is not None:
        print(f"  - Val samples: {X_val_t.shape[0]}")
    print(f"  - Test samples: {X_test_t.shape[0]}")
    print("\nArchivos generados:")
    print(f"  - preprocessor.pkl")
    print(f"  - feature_names.json")
    print(f"  - datasets_procesados.pkl")
    print("\nPróximo paso: Model Training (model_training_evaluation.py)")


if __name__ == "__main__":
    main()
