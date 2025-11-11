"""
Feature Engineering Module para MLOps Pipeline.

Este módulo implementa el procesamiento de características usando sklearn pipelines
de forma genérica y reutilizable para cualquier dataset tabular.

Flujo:
    1. Carga del dataset limpio desde el EDA
    2. Separación de features y target
    3. Split train/test
    4. Transformaciones con ColumnTransformer
    5. Exportación de datos procesados y pipeline
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    OneHotEncoder,
    LabelEncoder,
    PowerTransformer
)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Clase para realizar feature engineering de forma genérica y reutilizable.
    
    Attributes:
        project_root: Ruta raíz del proyecto
        metadata: Metadatos del EDA
        target_column: Nombre de la columna objetivo
        preprocessor: Pipeline de transformación
    """
    
    def __init__(self, project_root: Path):
        """
        Inicializa el FeatureEngineer.
        
        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.metadata = self._load_metadata()
        self.target_column = self.metadata.get('target_column', 'Exited')
        self.preprocessor: Optional[ColumnTransformer] = None
        logger.info("FeatureEngineer inicializado correctamente")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """
        Carga los metadatos del EDA.
        
        Returns:
            Diccionario con metadatos
        """
        metadata_path = self.project_root / 'data' / 'metadata' / 'eda_metadata.json'
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            logger.info("Metadatos del EDA cargados correctamente")
            return metadata
        except FileNotFoundError:
            logger.warning(f"No se encontró {metadata_path}, usando configuración por defecto")
            return {}
    
    def load_data(self) -> pd.DataFrame:
        """
        Carga el dataset limpio desde el EDA.
        
        Returns:
            DataFrame limpio
        """
        data_path = self.project_root / 'data' / 'processed' / 'data_cleaned.csv'
        
        if not data_path.exists():
            logger.warning(f"{data_path} no existe, cargando dataset original")
            data_path = self.project_root / 'data' / 'raw' / 'Churn_Modelling.csv'
        
        df = pd.read_csv(data_path)
        logger.info(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    
    def split_features_target(
        self, 
        df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separa features y variable objetivo.
        
        Args:
            df: DataFrame completo
        
        Returns:
            Tupla (X, y)
        """
        if self.target_column not in df.columns:
            raise ValueError(f"Columna objetivo '{self.target_column}' no encontrada")
        
        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]
        
        logger.info(f"Features: {X.shape[1]} columnas, Target: {self.target_column}")
        return X, y
    
    def identify_column_types(
        self, 
        X: pd.DataFrame
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Identifica tipos de columnas para aplicar transformaciones específicas.
        
        Args:
            X: DataFrame de features
        
        Returns:
            Tupla (numéricas_continuas, numéricas_discretas, categóricas)
        """
        numerical_continuous = []
        numerical_discrete = []
        categorical = []
        
        for col in X.columns:
            # Verificar si es numérico
            if X[col].dtype in ['int64', 'float64']:
                unique_vals = X[col].nunique()
                # Si tiene pocos valores únicos, es discreta
                if unique_vals <= 10:
                    numerical_discrete.append(col)
                else:
                    numerical_continuous.append(col)
            else:
                categorical.append(col)
        
        logger.info(f"Columnas identificadas - Continuas: {len(numerical_continuous)}, "
                   f"Discretas: {len(numerical_discrete)}, "
                   f"Categóricas: {len(categorical)}")
        
        return numerical_continuous, numerical_discrete, categorical
    
    def build_preprocessor(
        self,
        numerical_continuous: List[str],
        numerical_discrete: List[str],
        categorical: List[str],
        scaling_method: str = 'standard'
    ) -> ColumnTransformer:
        """
        Construye el pipeline de preprocesamiento.
        
        Args:
            numerical_continuous: Lista de columnas numéricas continuas
            numerical_discrete: Lista de columnas numéricas discretas
            categorical: Lista de columnas categóricas
            scaling_method: Método de escalado ('standard' o 'minmax')
        
        Returns:
            ColumnTransformer configurado
        """
        transformers = []
        
        # Pipeline para variables continuas
        if numerical_continuous:
            numerical_continuous_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler() if scaling_method == 'standard' 
                          else MinMaxScaler())
            ])
            transformers.append(
                ('num_continuous', numerical_continuous_pipeline, numerical_continuous)
            )
        
        # Pipeline para variables discretas
        if numerical_discrete:
            numerical_discrete_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('scaler', StandardScaler() if scaling_method == 'standard' 
                          else MinMaxScaler())
            ])
            transformers.append(
                ('num_discrete', numerical_discrete_pipeline, numerical_discrete)
            )
        
        # Pipeline para variables categóricas
        if categorical:
            categorical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
                ('onehot', OneHotEncoder(drop='first', sparse_output=False, 
                                        handle_unknown='ignore'))
            ])
            transformers.append(
                ('cat', categorical_pipeline, categorical)
            )
        
        preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder='passthrough'
        )
        
        logger.info("Preprocessor construido exitosamente")
        return preprocessor
    
    def fit_transform_data(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Ajusta y transforma los datos de entrenamiento y prueba.
        
        Args:
            X_train: Datos de entrenamiento
            X_test: Datos de prueba
        
        Returns:
            Tupla (X_train_transformed, X_test_transformed)
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor no ha sido construido. Ejecutar build_preprocessor() primero.")
        
        X_train_transformed = self.preprocessor.fit_transform(X_train)
        X_test_transformed = self.preprocessor.transform(X_test)
        
        logger.info(f"Datos transformados - Train: {X_train_transformed.shape}, "
                   f"Test: {X_test_transformed.shape}")
        
        return X_train_transformed, X_test_transformed
    
    def get_feature_names(self) -> List[str]:
        """
        Obtiene los nombres de las features después de la transformación.
        
        Returns:
            Lista de nombres de features
        """
        if self.preprocessor is None:
            return []
        
        feature_names = []
        
        for name, transformer, columns in self.preprocessor.transformers_:
            if name == 'remainder':
                continue
            
            if hasattr(transformer, 'get_feature_names_out'):
                names = transformer.get_feature_names_out(columns)
                feature_names.extend(names)
            else:
                feature_names.extend(columns)
        
        return feature_names
    
    def save_artifacts(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: pd.Series,
        y_test: pd.Series,
        feature_names: List[str]
    ) -> None:
        """
        Guarda los artefactos del feature engineering.
        
        Args:
            X_train: Features de entrenamiento transformadas
            X_test: Features de prueba transformadas
            y_train: Target de entrenamiento
            y_test: Target de prueba
            feature_names: Nombres de las features
        """
        # Guardar preprocessor
        preprocessor_path = self.project_root / 'models' / 'preprocessor.pkl'
        joblib.dump(self.preprocessor, preprocessor_path)
        logger.info(f"Preprocessor guardado en: {preprocessor_path}")
        
        # Guardar datasets procesados
        train_data = pd.DataFrame(X_train, columns=feature_names)
        train_data[self.target_column] = y_train.values
        train_path = self.project_root / 'data' / 'processed' / 'train_data.csv'
        train_data.to_csv(train_path, index=False)
        logger.info(f"Datos de entrenamiento guardados en: {train_path}")
        
        test_data = pd.DataFrame(X_test, columns=feature_names)
        test_data[self.target_column] = y_test.values
        test_path = self.project_root / 'data' / 'processed' / 'test_data.csv'
        test_data.to_csv(test_path, index=False)
        logger.info(f"Datos de prueba guardados en: {test_path}")
        
        # Guardar metadatos del feature engineering
        fe_metadata = {
            'target_column': self.target_column,
            'n_features': len(feature_names),
            'feature_names': feature_names,
            'train_shape': list(X_train.shape),
            'test_shape': list(X_test.shape)
        }
        
        metadata_path = self.project_root / 'data' / 'metadata' / 'feature_engineering_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(fe_metadata, f, indent=2)
        logger.info(f"Metadatos guardados en: {metadata_path}")


def main() -> None:
    """
    Función principal para ejecutar el feature engineering.
    """
    # Configurar rutas
    project_root = Path(__file__).parent.parent.parent
    
    print("="*70)
    print("FEATURE ENGINEERING - MLOps Pipeline")
    print("="*70)
    
    # Inicializar FeatureEngineer
    fe = FeatureEngineer(project_root)
    
    # 1. Cargar datos
    print("\n[1/6] Cargando datos...")
    df = fe.load_data()
    print(f"✓ Dataset cargado: {df.shape}")
    
    # 2. Separar features y target
    print("\n[2/6] Separando features y target...")
    X, y = fe.split_features_target(df)
    print(f"✓ Features: {X.shape}, Target: {y.shape}")
    
    # 3. Identificar tipos de columnas
    print("\n[3/6] Identificando tipos de columnas...")
    num_continuous, num_discrete, categorical = fe.identify_column_types(X)
    print(f"✓ Numéricas continuas: {len(num_continuous)}")
    print(f"✓ Numéricas discretas: {len(num_discrete)}")
    print(f"✓ Categóricas: {len(categorical)}")
    
    # 4. Split train/test
    print("\n[4/6] Dividiendo en train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✓ Train: {X_train.shape}, Test: {X_test.shape}")
    
    # 5. Construir y aplicar preprocessor
    print("\n[5/6] Construyendo y aplicando transformaciones...")
    fe.preprocessor = fe.build_preprocessor(
        num_continuous, num_discrete, categorical, scaling_method='standard'
    )
    X_train_transformed, X_test_transformed = fe.fit_transform_data(X_train, X_test)
    feature_names = fe.get_feature_names()
    print(f"✓ Transformaciones aplicadas")
    print(f"✓ Features finales: {len(feature_names)}")
    
    # 6. Guardar artefactos
    print("\n[6/6] Guardando artefactos...")
    fe.save_artifacts(
        X_train_transformed, X_test_transformed, 
        y_train, y_test, feature_names
    )
    print("✓ Artefactos guardados")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE FEATURE ENGINEERING")
    print("="*70)
    print(f"Features originales: {X.shape[1]}")
    print(f"Features transformadas: {len(feature_names)}")
    print(f"Registros entrenamiento: {X_train_transformed.shape[0]:,}")
    print(f"Registros prueba: {X_test_transformed.shape[0]:,}")
    print("\n✓ FEATURE ENGINEERING COMPLETADO")
    print("→ Continuar con model_training_evaluation.py")
    print("="*70)


if __name__ == "__main__":
    main()
