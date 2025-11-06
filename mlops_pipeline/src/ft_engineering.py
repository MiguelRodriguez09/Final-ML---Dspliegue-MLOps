"""
Feature Engineering Module - MLOps Pipeline

Este módulo contiene funciones reutilizables para:
- Limpieza y preprocesamiento de datos
- Codificación de variables categóricas
- Escalamiento de variables numéricas
- Separación train/test

Todas las funciones son GENERALIZABLES y funcionan con cualquier dataset.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
import warnings

warnings.filterwarnings('ignore')


def identificar_tipos_variables(df, target_col=None):
    """
    Identifica automáticamente los tipos de variables en el dataframe.
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
        target_col (str): Nombre de la columna objetivo (opcional)
    
    Returns:
        dict: Diccionario con listas de columnas por tipo
    """
    tipos = {
        'numericas_continuas': [],
        'numericas_discretas': [],
        'categoricas': [],
        'booleanas': [],
        'id_candidatas': []
    }
    
    columnas_analizar = [col for col in df.columns if col != target_col]
    
    for col in columnas_analizar:
        # Booleanas (binarias con 2 valores únicos)
        if df[col].nunique() == 2:
            tipos['booleanas'].append(col)
        
        # Numéricas
        elif pd.api.types.is_numeric_dtype(df[col]):
            # Detectar IDs (alta cardinalidad)
            if df[col].nunique() == len(df) or df[col].nunique() / len(df) > 0.95:
                tipos['id_candidatas'].append(col)
            # Discretas (enteros con pocos valores únicos)
            elif df[col].dtype in ['int64', 'int32'] and df[col].nunique() < 20:
                tipos['numericas_discretas'].append(col)
            # Continuas
            else:
                tipos['numericas_continuas'].append(col)
        
        # Categóricas
        elif df[col].dtype == 'object' or df[col].dtype.name == 'category':
            # Detectar texto libre (alta cardinalidad)
            if df[col].nunique() / len(df) > 0.5:
                tipos['id_candidatas'].append(col)
            else:
                tipos['categoricas'].append(col)
    
    return tipos


def eliminar_variables_irrelevantes(df, umbral_nulos=0.95, umbral_cardinalidad=0.95, verbose=True):
    """
    Elimina variables irrelevantes del dataset.
    
    Args:
        df (pd.DataFrame): DataFrame original
        umbral_nulos (float): Umbral de porcentaje de nulos para eliminar (default 0.95)
        umbral_cardinalidad (float): Umbral de cardinalidad para eliminar IDs (default 0.95)
        verbose (bool): Si True, muestra información de las columnas eliminadas
    
    Returns:
        pd.DataFrame: DataFrame sin variables irrelevantes
    """
    df_clean = df.copy()
    columnas_eliminadas = []
    razones = []
    
    for col in df.columns:
        pct_nulos = df[col].isnull().sum() / len(df)
        n_unicos = df[col].nunique()
        
        # Criterios de eliminación
        if pct_nulos > umbral_nulos:
            columnas_eliminadas.append(col)
            razones.append(f">{umbral_nulos*100}% valores nulos")
        elif n_unicos == 1:
            columnas_eliminadas.append(col)
            razones.append("Varianza cero")
        elif n_unicos == len(df) or n_unicos / len(df) > umbral_cardinalidad:
            columnas_eliminadas.append(col)
            razones.append(f"Cardinalidad muy alta ({n_unicos} valores únicos)")
    
    if columnas_eliminadas:
        df_clean = df_clean.drop(columns=columnas_eliminadas)
        
        if verbose:
            print(f"\n🗑️ Eliminadas {len(columnas_eliminadas)} columnas:")
            for col, razon in zip(columnas_eliminadas, razones):
                print(f"  - {col}: {razon}")
    else:
        if verbose:
            print("\n✅ No se eliminaron columnas irrelevantes")
    
    return df_clean


def imputar_valores_nulos(df, estrategia_numericas='median', estrategia_categoricas='most_frequent', verbose=True):
    """
    Imputa valores nulos usando estrategias apropiadas por tipo de variable.
    
    Args:
        df (pd.DataFrame): DataFrame con valores nulos
        estrategia_numericas (str): Estrategia para numéricas ('mean', 'median', 'most_frequent')
        estrategia_categoricas (str): Estrategia para categóricas ('most_frequent', 'constant')
        verbose (bool): Si True, muestra información del proceso
    
    Returns:
        pd.DataFrame: DataFrame sin valores nulos
    """
    df_clean = df.copy()
    
    # Identificar columnas con valores nulos
    cols_con_nulos = df_clean.columns[df_clean.isnull().any()].tolist()
    
    if not cols_con_nulos:
        if verbose:
            print("\n✅ No hay valores nulos para imputar")
        return df_clean
    
    if verbose:
        print(f"\n💉 Imputando valores nulos en {len(cols_con_nulos)} columnas...")
    
    # Separar por tipo
    cols_numericas = df_clean[cols_con_nulos].select_dtypes(include=[np.number]).columns.tolist()
    cols_categoricas = df_clean[cols_con_nulos].select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Imputar numéricas
    if cols_numericas:
        imputer_num = SimpleImputer(strategy=estrategia_numericas)
        df_clean[cols_numericas] = imputer_num.fit_transform(df_clean[cols_numericas])
        if verbose:
            print(f"  - Numéricas ({len(cols_numericas)}): {estrategia_numericas}")
    
    # Imputar categóricas
    if cols_categoricas:
        imputer_cat = SimpleImputer(strategy=estrategia_categoricas)
        df_clean[cols_categoricas] = imputer_cat.fit_transform(df_clean[cols_categoricas])
        if verbose:
            print(f"  - Categóricas ({len(cols_categoricas)}): {estrategia_categoricas}")
    
    return df_clean


def codificar_categoricas(df, metodo='auto', max_categorias_onehot=10, verbose=True):
    """
    Codifica variables categóricas usando Label Encoding o One-Hot Encoding.
    
    Args:
        df (pd.DataFrame): DataFrame con variables categóricas
        metodo (str): 'label', 'onehot', o 'auto' (decide automáticamente)
        max_categorias_onehot (int): Máximo de categorías para usar one-hot
        verbose (bool): Si True, muestra información del proceso
    
    Returns:
        pd.DataFrame: DataFrame con variables codificadas
    """
    df_encoded = df.copy()
    
    # Identificar columnas categóricas
    cols_categoricas = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not cols_categoricas:
        if verbose:
            print("\n✅ No hay variables categóricas para codificar")
        return df_encoded
    
    if verbose:
        print(f"\n🔤 Codificando {len(cols_categoricas)} variables categóricas...")
    
    for col in cols_categoricas:
        n_categorias = df_encoded[col].nunique()
        
        # Decidir método automáticamente
        if metodo == 'auto':
            usar_onehot = n_categorias <= max_categorias_onehot
        elif metodo == 'onehot':
            usar_onehot = True
        else:
            usar_onehot = False
        
        if usar_onehot:
            # One-Hot Encoding
            dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=True)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            df_encoded = df_encoded.drop(columns=[col])
            
            if verbose:
                print(f"  - {col}: One-Hot Encoding ({n_categorias} categorías -> {len(dummies.columns)} columnas)")
        else:
            # Label Encoding
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            
            if verbose:
                print(f"  - {col}: Label Encoding ({n_categorias} categorías)")
    
    return df_encoded


def escalar_numericas(df, metodo='standard', excluir_columnas=None, verbose=True):
    """
    Escala variables numéricas usando StandardScaler o MinMaxScaler.
    
    Args:
        df (pd.DataFrame): DataFrame con variables numéricas
        metodo (str): 'standard' (estandarización) o 'minmax' (normalización 0-1)
        excluir_columnas (list): Lista de columnas a excluir del escalamiento
        verbose (bool): Si True, muestra información del proceso
    
    Returns:
        tuple: (DataFrame escalado, scaler utilizado)
    """
    df_scaled = df.copy()
    
    if excluir_columnas is None:
        excluir_columnas = []
    
    # Identificar columnas numéricas
    cols_numericas = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
    cols_a_escalar = [col for col in cols_numericas if col not in excluir_columnas]
    
    if not cols_a_escalar:
        if verbose:
            print("\n✅ No hay variables numéricas para escalar")
        return df_scaled, None
    
    if verbose:
        print(f"\n📏 Escalando {len(cols_a_escalar)} variables numéricas usando {metodo}...")
    
    # Seleccionar scaler
    if metodo == 'standard':
        scaler = StandardScaler()
    elif metodo == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError("Método debe ser 'standard' o 'minmax'")
    
    # Aplicar escalamiento
    df_scaled[cols_a_escalar] = scaler.fit_transform(df_scaled[cols_a_escalar])
    
    return df_scaled, scaler


def separar_train_test(df, target_col, test_size=0.2, random_state=42, stratify=True, verbose=True):
    """
    Separa el dataset en conjuntos de entrenamiento y prueba.
    
    Args:
        df (pd.DataFrame): DataFrame completo
        target_col (str): Nombre de la columna objetivo
        test_size (float): Proporción del conjunto de prueba (default 0.2)
        random_state (int): Semilla para reproducibilidad
        stratify (bool): Si True, mantiene la proporción de clases en la separación
        verbose (bool): Si True, muestra información del proceso
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    if target_col not in df.columns:
        raise ValueError(f"La columna objetivo '{target_col}' no existe en el DataFrame")
    
    # Separar características y objetivo
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Determinar si usar stratify
    stratify_param = y if stratify and y.nunique() < 20 else None
    
    # Separar
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=stratify_param
    )
    
    if verbose:
        print(f"\n✂️ Separación Train/Test:")
        print(f"  - Train: {len(X_train)} muestras ({(1-test_size)*100:.1f}%)")
        print(f"  - Test: {len(X_test)} muestras ({test_size*100:.1f}%)")
        
        if stratify_param is not None:
            print(f"\n  Distribución de clases (Train):")
            for clase, count in y_train.value_counts().items():
                print(f"    {clase}: {count} ({count/len(y_train)*100:.2f}%)")
    
    return X_train, X_test, y_train, y_test


def pipeline_preprocesamiento_completo(df, target_col, 
                                       eliminar_irrelevantes=True,
                                       imputar_nulos=True,
                                       codificar_cats=True,
                                       escalar_nums=True,
                                       test_size=0.2,
                                       random_state=42):
    """
    Pipeline completo de preprocesamiento de datos.
    
    Args:
        df (pd.DataFrame): DataFrame original
        target_col (str): Nombre de la columna objetivo
        eliminar_irrelevantes (bool): Si True, elimina columnas irrelevantes
        imputar_nulos (bool): Si True, imputa valores nulos
        codificar_cats (bool): Si True, codifica variables categóricas
        escalar_nums (bool): Si True, escala variables numéricas
        test_size (float): Proporción del conjunto de prueba
        random_state (int): Semilla para reproducibilidad
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler, info_preprocesamiento)
    """
    print("\n" + "="*70)
    print("🔧 PIPELINE DE PREPROCESAMIENTO")
    print("="*70)
    
    df_processed = df.copy()
    info = {
        'columnas_originales': df.shape[1],
        'filas_originales': df.shape[0],
        'columnas_eliminadas': [],
        'columnas_finales': None,
        'metodo_imputacion': None,
        'metodo_codificacion': None,
        'metodo_escalamiento': None
    }
    
    # 1. Eliminar variables irrelevantes (excepto target)
    if eliminar_irrelevantes:
        cols_antes = df_processed.shape[1]
        # Guardar target temporalmente
        target_data = df_processed[target_col].copy()
        df_processed = df_processed.drop(columns=[target_col])
        
        df_processed = eliminar_variables_irrelevantes(df_processed)
        
        # Restaurar target
        df_processed[target_col] = target_data
        
        info['columnas_eliminadas'] = cols_antes - df_processed.shape[1]
    
    # 2. Imputar valores nulos
    if imputar_nulos:
        df_processed = imputar_valores_nulos(df_processed, estrategia_numericas='median')
        info['metodo_imputacion'] = 'median (numéricas) / most_frequent (categóricas)'
    
    # 3. Codificar categóricas (excepto target)
    if codificar_cats:
        # Guardar target temporalmente
        target_data = df_processed[target_col].copy()
        df_processed = df_processed.drop(columns=[target_col])
        
        df_processed = codificar_categoricas(df_processed, metodo='auto', max_categorias_onehot=10)
        
        # Restaurar target
        df_processed[target_col] = target_data
        
        info['metodo_codificacion'] = 'auto (One-Hot o Label según categorías)'
    
    # 4. Separar train/test
    X_train, X_test, y_train, y_test = separar_train_test(
        df_processed, target_col, test_size=test_size, random_state=random_state
    )
    
    # 5. Escalar numéricas (solo en train, aplicar a test)
    scaler = None
    if escalar_nums:
        X_train_scaled, scaler = escalar_numericas(X_train, metodo='standard')
        X_test_scaled = X_test.copy()
        
        # Aplicar el mismo escalamiento a test
        cols_numericas = X_train.select_dtypes(include=[np.number]).columns.tolist()
        if cols_numericas:
            X_test_scaled[cols_numericas] = scaler.transform(X_test[cols_numericas])
        
        X_train = X_train_scaled
        X_test = X_test_scaled
        
        info['metodo_escalamiento'] = 'StandardScaler'
    
    info['columnas_finales'] = X_train.shape[1]
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DEL PREPROCESAMIENTO")
    print("="*70)
    print(f"Columnas originales: {info['columnas_originales']}")
    print(f"Columnas finales: {info['columnas_finales']}")
    print(f"Filas totales: {info['filas_originales']}")
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")
    print("\n✅ Preprocesamiento completado exitosamente")
    
    return X_train, X_test, y_train, y_test, scaler, info


# Ejemplo de uso
if __name__ == "__main__":
    """
    Ejemplo de uso del módulo con un dataset genérico.
    """
    import os
    
    # Cargar datos
    ruta_datos = os.path.join('..', '..', 'base_de_datos.csv')
    df = pd.read_csv(ruta_datos)
    
    print(f"Dataset cargado: {df.shape}")
    
    # Detectar variable objetivo automáticamente
    posibles_targets = [col for col in df.columns if any(keyword in col.lower() 
                       for keyword in ['target', 'label', 'exited', 'churn', 'class'])]
    
    if posibles_targets:
        target_col = posibles_targets[0]
        print(f"Variable objetivo detectada: {target_col}")
        
        # Aplicar pipeline completo
        X_train, X_test, y_train, y_test, scaler, info = pipeline_preprocesamiento_completo(
            df, 
            target_col=target_col,
            test_size=0.2,
            random_state=42
        )
        
        print(f"\n✅ Datos listos para entrenamiento")
        print(f"X_train shape: {X_train.shape}")
        print(f"X_test shape: {X_test.shape}")
    else:
        print("⚠️ No se detectó variable objetivo. Especifica 'target_col' manualmente.")
