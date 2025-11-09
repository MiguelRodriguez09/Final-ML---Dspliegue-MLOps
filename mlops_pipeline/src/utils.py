"""
Utilidades comunes para el proyecto MLOps.

Este módulo contiene funciones auxiliares reutilizables en todo el proyecto.

Autor: MLOps Pipeline
Fecha: 2025
"""

import json
import pickle
import logging
from pathlib import Path
from typing import Any, Dict, Union
import numpy as np
import pandas as pd


def setup_logger(name: str, log_file: Path = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configura y retorna un logger.
    
    Args:
        name: Nombre del logger
        log_file: Archivo de log (opcional)
        level: Nivel de logging
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (opcional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def convert_numpy_to_python(obj: Any) -> Any:
    """
    Convierte tipos NumPy a tipos nativos de Python para serialización JSON.
    
    Args:
        obj: Objeto a convertir
        
    Returns:
        Any: Objeto convertido a tipo Python nativo
    """
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {key: convert_numpy_to_python(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [convert_numpy_to_python(item) for item in obj]
    return obj


def guardar_json(data: Dict, filepath: Path, indent: int = 2) -> None:
    """
    Guarda un diccionario en formato JSON con manejo de tipos NumPy.
    
    Args:
        data: Diccionario a guardar
        filepath: Ruta del archivo
        indent: Indentación del JSON
        
    Raises:
        IOError: Si no se puede escribir el archivo
    """
    try:
        data_serializable = convert_numpy_to_python(data)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_serializable, f, indent=indent, ensure_ascii=False)
    except (IOError, OSError) as e:
        raise IOError(f"Error al guardar JSON en {filepath}: {str(e)}") from e


def cargar_json(filepath: Path) -> Dict:
    """
    Carga un archivo JSON.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Dict: Datos cargados
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el archivo no es JSON válido
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Error al decodificar JSON en {filepath}",
            e.doc,
            e.pos
        ) from e


def guardar_pickle(obj: Any, filepath: Path) -> None:
    """
    Guarda un objeto en formato pickle.
    
    Args:
        obj: Objeto a guardar
        filepath: Ruta del archivo
        
    Raises:
        IOError: Si no se puede escribir el archivo
    """
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
    except (IOError, OSError) as e:
        raise IOError(f"Error al guardar pickle en {filepath}: {str(e)}") from e


def cargar_pickle(filepath: Path) -> Any:
    """
    Carga un objeto desde un archivo pickle.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Any: Objeto cargado
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        pickle.UnpicklingError: Si hay error al deserializar
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except pickle.UnpicklingError as e:
        raise pickle.UnpicklingError(
            f"Error al cargar pickle desde {filepath}"
        ) from e


def validar_dataframe(
    df: pd.DataFrame,
    required_columns: list = None,
    min_rows: int = 1
) -> tuple:
    """
    Valida que un DataFrame cumpla con requisitos mínimos.
    
    Args:
        df: DataFrame a validar
        required_columns: Columnas requeridas (opcional)
        min_rows: Número mínimo de filas
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not isinstance(df, pd.DataFrame):
        return False, "El objeto no es un DataFrame"
    
    if len(df) < min_rows:
        return False, f"DataFrame tiene menos de {min_rows} filas"
    
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            return False, f"Faltan columnas requeridas: {missing_cols}"
    
    return True, None


def calcular_estadisticas_basicas(df: pd.DataFrame, columna: str) -> Dict:
    """
    Calcula estadísticas básicas para una columna.
    
    Args:
        df: DataFrame
        columna: Nombre de la columna
        
    Returns:
        Dict: Estadísticas de la columna
        
    Raises:
        KeyError: Si la columna no existe
    """
    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no encontrada en DataFrame")
    
    serie = df[columna].dropna()
    
    if pd.api.types.is_numeric_dtype(serie):
        return {
            'count': int(len(serie)),
            'mean': float(serie.mean()),
            'std': float(serie.std()),
            'min': float(serie.min()),
            'q25': float(serie.quantile(0.25)),
            'median': float(serie.median()),
            'q75': float(serie.quantile(0.75)),
            'max': float(serie.max()),
            'missing': int(df[columna].isna().sum())
        }
    
    return {
        'count': int(len(serie)),
        'unique': int(serie.nunique()),
        'top': str(serie.mode().iloc[0]) if not serie.mode().empty else None,
        'freq': int(serie.value_counts().iloc[0]) if not serie.value_counts().empty else 0,
        'missing': int(df[columna].isna().sum())
    }


def imprimir_seccion(titulo: str, ancho: int = 80, char: str = '=') -> None:
    """
    Imprime un título de sección formateado.
    
    Args:
        titulo: Título de la sección
        ancho: Ancho de la línea
        char: Carácter para la línea
    """
    print(f"\n{char * ancho}")
    print(titulo.center(ancho))
    print(f"{char * ancho}\n")


def crear_estructura_directorios(base_path: Path, subdirs: list) -> None:
    """
    Crea una estructura de directorios.
    
    Args:
        base_path: Ruta base
        subdirs: Lista de subdirectorios a crear
    """
    for subdir in subdirs:
        dir_path = base_path / subdir
        dir_path.mkdir(parents=True, exist_ok=True)


def obtener_tipo_variable(serie: pd.Series) -> str:
    """
    Determina el tipo de variable (numérica, categórica, etc.).
    
    Args:
        serie: Serie de pandas
        
    Returns:
        str: Tipo de variable ('numeric', 'categorical', 'datetime', 'other')
    """
    if pd.api.types.is_numeric_dtype(serie):
        return 'numeric'
    if pd.api.types.is_datetime64_any_dtype(serie):
        return 'datetime'
    if pd.api.types.is_categorical_dtype(serie) or pd.api.types.is_object_dtype(serie):
        return 'categorical'
    return 'other'


def limpiar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia los nombres de las columnas de un DataFrame.
    
    Args:
        df: DataFrame
        
    Returns:
        pd.DataFrame: DataFrame con columnas renombradas
    """
    df_clean = df.copy()
    df_clean.columns = (
        df_clean.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('[^a-z0-9_]', '', regex=True)
    )
    return df_clean


def formatear_tiempo(segundos: float) -> str:
    """
    Formatea tiempo en segundos a formato legible.
    
    Args:
        segundos: Tiempo en segundos
        
    Returns:
        str: Tiempo formateado (ej: "2m 30s")
    """
    if segundos < 60:
        return f"{segundos:.2f}s"
    if segundos < 3600:
        minutos = int(segundos // 60)
        segs = int(segundos % 60)
        return f"{minutos}m {segs}s"
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    return f"{horas}h {minutos}m"


def porcentaje_cambio(valor_anterior: float, valor_actual: float) -> float:
    """
    Calcula el porcentaje de cambio entre dos valores.
    
    Args:
        valor_anterior: Valor anterior
        valor_actual: Valor actual
        
    Returns:
        float: Porcentaje de cambio
    """
    if valor_anterior == 0:
        return float('inf') if valor_actual != 0 else 0.0
    return ((valor_actual - valor_anterior) / abs(valor_anterior)) * 100
