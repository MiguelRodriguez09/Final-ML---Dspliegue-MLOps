"""
Model Training and Evaluation - MLOps Project

Este módulo implementa el entrenamiento y evaluación de múltiples modelos de ML,
con funciones genéricas y reutilizables para clasificación y regresión.

Características principales:
- Entrenamiento de múltiples modelos
- Evaluación comparativa con métricas estándar
- Selección del mejor modelo basado en performance, consistency y scalability
- Generación de reportes y visualizaciones
- Guardado del modelo seleccionado

Autor: MLOps Pipeline
Fecha: 2025
"""

import pandas as pd
import numpy as np
import pickle
import json
import joblib
from pathlib import Path
from typing import Dict, List, Tuple, Any
import time
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn imports
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# Metrics
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score
)

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns

# XGBoost y LightGBM (si están instalados)
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠ XGBoost no está instalado")

try:
    from lightgbm import LGBMClassifier
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("⚠ LightGBM no está instalado")


class ModelTrainer:
    """
    Clase para entrenar y evaluar múltiples modelos de ML.
    """
    
    def __init__(self, project_root: Path, task_type: str = 'classification'):
        """
        Inicializa el trainer de modelos.
        
        Parámetros:
        -----------
        project_root : Path
            Ruta raíz del proyecto
        task_type : str
            Tipo de tarea ('classification' o 'regression')
        """
        self.project_root = Path(project_root)
        self.task_type = task_type
        self.models_dir = self.project_root / 'mlops_pipeline' / 'models'
        self.processed_dir = self.project_root / 'mlops_pipeline' / 'data' / 'processed'
        self.reports_dir = self.project_root / 'mlops_pipeline' / 'reports'
        
        # Crear directorios
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.resultados = {}
        self.mejor_modelo = None
        
    def cargar_datasets(self) -> Tuple:
        """
        Carga los datasets procesados.
        
        Retorna:
        --------
        tuple : (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        ruta = self.processed_dir / 'datasets_procesados.pkl'
        
        if not ruta.exists():
            raise FileNotFoundError(f"El archivo {ruta} no existe. Ejecuta ft_engineering.py primero.")
        
        with open(ruta, 'rb') as f:
            datasets = pickle.load(f)
        
        print("✓ Datasets cargados exitosamente")
        print(f"  - X_train: {datasets['X_train'].shape}")
        if 'X_val' in datasets:
            print(f"  - X_val: {datasets['X_val'].shape}")
        print(f"  - X_test: {datasets['X_test'].shape}")
        
        X_val = datasets.get('X_val', None)
        y_val = datasets.get('y_val', None)
        
        return (datasets['X_train'], X_val, datasets['X_test'],
                datasets['y_train'], y_val, datasets['y_test'])
    
    def obtener_modelos_clasificacion(self) -> Dict:
        """
        Retorna un diccionario de modelos de clasificación preconfigurados.
        
        Retorna:
        --------
        dict : Diccionario de modelos
        """
        modelos = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=42, n_jobs=-1
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=10, random_state=42
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100, max_depth=5, random_state=42
            ),
            'SVM': SVC(
                kernel='rbf', probability=True, random_state=42
            ),
            'K-Nearest Neighbors': KNeighborsClassifier(
                n_neighbors=5, n_jobs=-1
            ),
            'Naive Bayes': GaussianNB()
        }
        
        # Agregar XGBoost si está disponible
        if XGBOOST_AVAILABLE:
            modelos['XGBoost'] = XGBClassifier(
                n_estimators=100, max_depth=5, random_state=42,
                eval_metric='logloss', use_label_encoder=False
            )
        
        # Agregar LightGBM si está disponible
        if LIGHTGBM_AVAILABLE:
            modelos['LightGBM'] = LGBMClassifier(
                n_estimators=100, max_depth=5, random_state=42, verbose=-1
            )
        
        return modelos
    
    def entrenar_modelo(self, 
                       modelo, 
                       X_train, y_train,
                       X_val=None, y_val=None,
                       nombre_modelo: str = 'Modelo') -> Dict:
        """
        Entrena un modelo y registra métricas de tiempo.
        
        Parámetros:
        -----------
        modelo : estimator
            Modelo de sklearn a entrenar
        X_train, y_train : arrays
            Datos de entrenamiento
        X_val, y_val : arrays, opcional
            Datos de validación
        nombre_modelo : str
            Nombre del modelo
            
        Retorna:
        --------
        dict : Diccionario con el modelo entrenado y métricas de entrenamiento
        """
        print(f"\n{'='*60}")
        print(f"Entrenando: {nombre_modelo}")
        print(f"{'='*60}")
        
        # Entrenar modelo
        inicio = time.time()
        modelo.fit(X_train, y_train)
        tiempo_entrenamiento = time.time() - inicio
        
        print(f"✓ Entrenamiento completado en {tiempo_entrenamiento:.2f} segundos")
        
        resultado = {
            'modelo': modelo,
            'nombre': nombre_modelo,
            'tiempo_entrenamiento': tiempo_entrenamiento
        }
        
        return resultado
    
    def evaluar_clasificacion(self,
                             modelo,
                             X_train, y_train,
                             X_val, y_val,
                             X_test, y_test,
                             nombre_modelo: str) -> Dict:
        """
        Evalúa un modelo de clasificación en todos los conjuntos.
        
        Parámetros:
        -----------
        modelo : estimator
            Modelo entrenado
        X_train, y_train : arrays
            Datos de entrenamiento
        X_val, y_val : arrays
            Datos de validación
        X_test, y_test : arrays
            Datos de prueba
        nombre_modelo : str
            Nombre del modelo
            
        Retorna:
        --------
        dict : Diccionario con todas las métricas
        """
        metricas = {'nombre': nombre_modelo}
        
        # Predecir en cada conjunto
        y_train_pred = modelo.predict(X_train)
        y_val_pred = modelo.predict(X_val) if X_val is not None else None
        y_test_pred = modelo.predict(X_test)
        
        # Probabilidades (si está disponible)
        try:
            y_train_proba = modelo.predict_proba(X_train)[:, 1]
            y_val_proba = modelo.predict_proba(X_val)[:, 1] if X_val is not None else None
            y_test_proba = modelo.predict_proba(X_test)[:, 1]
            tiene_proba = True
        except:
            tiene_proba = False
        
        # Calcular métricas para cada conjunto
        for conjunto, y_true, y_pred in [
            ('train', y_train, y_train_pred),
            ('val', y_val, y_val_pred),
            ('test', y_test, y_test_pred)
        ]:
            if y_true is None:
                continue
            
            metricas[f'{conjunto}_accuracy'] = accuracy_score(y_true, y_pred)
            metricas[f'{conjunto}_precision'] = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            metricas[f'{conjunto}_recall'] = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            metricas[f'{conjunto}_f1'] = f1_score(y_true, y_pred, average='weighted', zero_division=0)
            
            # AUC-ROC si hay probabilidades
            if tiene_proba:
                if conjunto == 'train':
                    proba = y_train_proba
                elif conjunto == 'val':
                    proba = y_val_proba
                else:
                    proba = y_test_proba
                
                if proba is not None and len(np.unique(y_true)) == 2:
                    metricas[f'{conjunto}_auc_roc'] = roc_auc_score(y_true, proba)
        
        # Calcular consistency (diferencia entre train y test)
        metricas['consistency'] = abs(metricas['train_accuracy'] - metricas['test_accuracy'])
        
        return metricas
    
    def summarize_classification(self, resultados: List[Dict]) -> pd.DataFrame:
        """
        Crea una tabla resumen de los resultados de clasificación.
        
        Parámetros:
        -----------
        resultados : list
            Lista de diccionarios con resultados de cada modelo
            
        Retorna:
        --------
        pd.DataFrame : Tabla resumen
        """
        df_resultados = pd.DataFrame(resultados)
        
        # Ordenar por F1-Score en test
        if 'test_f1' in df_resultados.columns:
            df_resultados = df_resultados.sort_values('test_f1', ascending=False)
        
        print("\n" + "="*100)
        print("RESUMEN DE RESULTADOS - MODELOS DE CLASIFICACIÓN")
        print("="*100)
        print(df_resultados.to_string())
        
        return df_resultados
    
    def build_model(self, 
                   X_train, y_train,
                   X_val, y_val,
                   X_test, y_test,
                   modelos_dict: Dict = None) -> Tuple[Dict, pd.DataFrame]:
        """
        Entrena y evalúa múltiples modelos.
        
        Parámetros:
        -----------
        X_train, y_train : arrays
            Datos de entrenamiento
        X_val, y_val : arrays
            Datos de validación
        X_test, y_test : arrays
            Datos de prueba
        modelos_dict : dict, opcional
            Diccionario de modelos personalizados
            
        Retorna:
        --------
        tuple : (resultados_dict, df_resumen)
        """
        if modelos_dict is None:
            if self.task_type == 'classification':
                modelos_dict = self.obtener_modelos_clasificacion()
            else:
                raise NotImplementedError("Solo clasificación está implementada actualmente")
        
        resultados_lista = []
        
        print("\n" + "="*100)
        print("INICIANDO ENTRENAMIENTO Y EVALUACIÓN DE MODELOS")
        print("="*100)
        
        for nombre, modelo in modelos_dict.items():
            # Entrenar
            resultado_entrenamiento = self.entrenar_modelo(
                modelo, X_train, y_train, X_val, y_val, nombre
            )
            
            # Evaluar
            if self.task_type == 'classification':
                metricas = self.evaluar_clasificacion(
                    resultado_entrenamiento['modelo'],
                    X_train, y_train,
                    X_val, y_val,
                    X_test, y_test,
                    nombre
                )
            
            # Combinar resultados
            resultado_completo = {**resultado_entrenamiento, **metricas}
            resultados_lista.append(resultado_completo)
            self.resultados[nombre] = resultado_completo
        
        # Crear resumen
        df_resumen = self.summarize_classification(resultados_lista)
        
        return self.resultados, df_resumen
    
    def seleccionar_mejor_modelo(self, 
                                 df_resumen: pd.DataFrame,
                                 metrica_principal: str = 'test_f1',
                                 umbral_consistency: float = 0.1) -> Dict:
        """
        Selecciona el mejor modelo basado en performance, consistency y scalability.
        
        Parámetros:
        -----------
        df_resumen : pd.DataFrame
            DataFrame con resultados de todos los modelos
        metrica_principal : str
            Métrica principal para selección
        umbral_consistency : float
            Umbral máximo de diferencia entre train y test
            
        Retorna:
        --------
        dict : Información del mejor modelo
        """
        print("\n" + "="*100)
        print("SELECCIÓN DEL MEJOR MODELO")
        print("="*100)
        
        # Filtrar por consistency
        df_filtered = df_resumen[df_resumen['consistency'] <= umbral_consistency].copy()
        
        if len(df_filtered) == 0:
            print(f"⚠ Ningún modelo cumple el umbral de consistency ({umbral_consistency})")
            print("  Seleccionando el mejor modelo sin filtro de consistency...")
            df_filtered = df_resumen.copy()
        
        # Seleccionar por métrica principal
        mejor_idx = df_filtered[metrica_principal].idxmax()
        mejor_modelo_info = df_filtered.loc[mejor_idx]
        
        nombre_mejor = mejor_modelo_info['nombre']
        self.mejor_modelo = self.resultados[nombre_mejor]
        
        print(f"\n✓ Mejor Modelo: {nombre_mejor}")
        print(f"\nMétricas principales:")
        print(f"  - Test Accuracy: {mejor_modelo_info.get('test_accuracy', 0):.4f}")
        print(f"  - Test Precision: {mejor_modelo_info.get('test_precision', 0):.4f}")
        print(f"  - Test Recall: {mejor_modelo_info.get('test_recall', 0):.4f}")
        print(f"  - Test F1-Score: {mejor_modelo_info.get('test_f1', 0):.4f}")
        if 'test_auc_roc' in mejor_modelo_info:
            print(f"  - Test AUC-ROC: {mejor_modelo_info.get('test_auc_roc', 0):.4f}")
        print(f"  - Consistency: {mejor_modelo_info['consistency']:.4f}")
        print(f"  - Tiempo de entrenamiento: {mejor_modelo_info['tiempo_entrenamiento']:.2f}s")
        
        return self.mejor_modelo
    
    def visualizar_comparacion(self, df_resumen: pd.DataFrame):
        """
        Genera gráficos comparativos de los modelos.
        
        Parámetros:
        -----------
        df_resumen : pd.DataFrame
            DataFrame con resultados
        """
        print("\n" + "="*100)
        print("GENERANDO VISUALIZACIONES COMPARATIVAS")
        print("="*100)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Comparación de métricas en test
        ax1 = axes[0, 0]
        metricas_test = ['test_accuracy', 'test_precision', 'test_recall', 'test_f1']
        metricas_disponibles = [m for m in metricas_test if m in df_resumen.columns]
        
        df_plot = df_resumen[['nombre'] + metricas_disponibles].set_index('nombre')
        df_plot.plot(kind='bar', ax=ax1)
        ax1.set_title('Comparación de Métricas en Test Set', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Modelo')
        ax1.set_ylabel('Score')
        ax1.legend(title='Métricas')
        ax1.grid(axis='y', alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 2. Train vs Test Accuracy
        ax2 = axes[0, 1]
        if 'train_accuracy' in df_resumen.columns and 'test_accuracy' in df_resumen.columns:
            x = np.arange(len(df_resumen))
            width = 0.35
            ax2.bar(x - width/2, df_resumen['train_accuracy'], width, label='Train', alpha=0.8)
            ax2.bar(x + width/2, df_resumen['test_accuracy'], width, label='Test', alpha=0.8)
            ax2.set_title('Train vs Test Accuracy', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Modelo')
            ax2.set_ylabel('Accuracy')
            ax2.set_xticks(x)
            ax2.set_xticklabels(df_resumen['nombre'], rotation=45, ha='right')
            ax2.legend()
            ax2.grid(axis='y', alpha=0.3)
        
        # 3. Consistency (Overfitting)
        ax3 = axes[1, 0]
        if 'consistency' in df_resumen.columns:
            df_resumen.plot(x='nombre', y='consistency', kind='bar', ax=ax3, color='coral', legend=False)
            ax3.axhline(y=0.1, color='r', linestyle='--', label='Umbral (0.1)')
            ax3.set_title('Consistency (Train-Test Gap)', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Modelo')
            ax3.set_ylabel('Diferencia Absoluta')
            ax3.legend()
            ax3.grid(axis='y', alpha=0.3)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 4. Tiempo de entrenamiento
        ax4 = axes[1, 1]
        if 'tiempo_entrenamiento' in df_resumen.columns:
            df_resumen.plot(x='nombre', y='tiempo_entrenamiento', kind='barh', ax=ax4, color='skyblue', legend=False)
            ax4.set_title('Tiempo de Entrenamiento (segundos)', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Tiempo (s)')
            ax4.set_ylabel('Modelo')
            ax4.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar figura
        ruta_fig = self.reports_dir / 'comparacion_modelos.png'
        plt.savefig(ruta_fig, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado en: {ruta_fig}")
        
        plt.show()
    
    def generar_matriz_confusion(self, X_test, y_test):
        """
        Genera la matriz de confusión del mejor modelo.
        
        Parámetros:
        -----------
        X_test, y_test : arrays
            Datos de prueba
        """
        if self.mejor_modelo is None:
            print("⚠ No hay modelo seleccionado")
            return
        
        modelo = self.mejor_modelo['modelo']
        y_pred = modelo.predict(X_test)
        
        # Calcular matriz de confusión
        cm = confusion_matrix(y_test, y_pred)
        
        # Visualizar
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
        plt.title(f"Matriz de Confusión - {self.mejor_modelo['nombre']}", 
                 fontsize=14, fontweight='bold')
        plt.ylabel('Valor Real')
        plt.xlabel('Valor Predicho')
        
        # Guardar
        ruta_fig = self.reports_dir / 'matriz_confusion.png'
        plt.savefig(ruta_fig, dpi=300, bbox_inches='tight')
        print(f"✓ Matriz de confusión guardada en: {ruta_fig}")
        
        plt.show()
        
        # Reporte de clasificación
        print("\n" + "="*80)
        print("REPORTE DE CLASIFICACIÓN - MEJOR MODELO")
        print("="*80)
        print(classification_report(y_test, y_pred))
    
    def guardar_mejor_modelo(self, nombre_archivo: str = 'best_model.pkl'):
        """
        Guarda el mejor modelo entrenado.
        
        Parámetros:
        -----------
        nombre_archivo : str
            Nombre del archivo de salida
        """
        if self.mejor_modelo is None:
            print("⚠ No hay modelo seleccionado para guardar")
            return
        
        ruta = self.models_dir / nombre_archivo
        joblib.dump(self.mejor_modelo['modelo'], ruta)
        
        # Guardar metadata
        metadata = {
            'nombre': self.mejor_modelo['nombre'],
            'metricas': {k: v for k, v in self.mejor_modelo.items() 
                        if k not in ['modelo']},
            'fecha_entrenamiento': pd.Timestamp.now().isoformat()
        }
        
        ruta_metadata = self.models_dir / 'best_model_metadata.json'
        with open(ruta_metadata, 'w') as f:
            # Convertir valores numpy a Python nativo
            metadata_serializable = json.loads(
                json.dumps(metadata, default=lambda x: float(x) if isinstance(x, (np.integer, np.floating)) else str(x))
            )
            json.dump(metadata_serializable, f, indent=2)
        
        print(f"\n✓ Mejor modelo guardado en: {ruta}")
        print(f"✓ Metadata guardada en: {ruta_metadata}")
    
    def guardar_resultados(self, df_resumen: pd.DataFrame):
        """
        Guarda los resultados en formato CSV y JSON.
        
        Parámetros:
        -----------
        df_resumen : pd.DataFrame
            DataFrame con resultados
        """
        # Guardar CSV
        ruta_csv = self.reports_dir / 'resultados_modelos.csv'
        df_resumen.to_csv(ruta_csv, index=False)
        print(f"✓ Resultados guardados en CSV: {ruta_csv}")
        
        # Guardar JSON
        ruta_json = self.reports_dir / 'resultados_modelos.json'
        resultados_dict = df_resumen.to_dict(orient='records')
        with open(ruta_json, 'w') as f:
            json.dump(resultados_dict, f, indent=2, default=lambda x: float(x) if isinstance(x, (np.integer, np.floating)) else str(x))
        print(f"✓ Resultados guardados en JSON: {ruta_json}")


def main():
    """
    Función principal para ejecutar el pipeline de entrenamiento y evaluación.
    """
    # Configuración
    project_root = Path(__file__).parent.parent.parent
    
    print("="*100)
    print("MODEL TRAINING AND EVALUATION PIPELINE")
    print("="*100)
    
    # Inicializar trainer
    trainer = ModelTrainer(project_root, task_type='classification')
    
    # 1. Cargar datasets
    print("\n[1/7] Cargando datasets...")
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.cargar_datasets()
    
    # 2. Construir y entrenar modelos
    print("\n[2/7] Construyendo y entrenando modelos...")
    resultados, df_resumen = trainer.build_model(
        X_train, y_train,
        X_val, y_val,
        X_test, y_test
    )
    
    # 3. Seleccionar mejor modelo
    print("\n[3/7] Seleccionando mejor modelo...")
    mejor_modelo = trainer.seleccionar_mejor_modelo(df_resumen)
    
    # 4. Visualizar comparaciones
    print("\n[4/7] Generando visualizaciones...")
    trainer.visualizar_comparacion(df_resumen)
    
    # 5. Matriz de confusión
    print("\n[5/7] Generando matriz de confusión...")
    trainer.generar_matriz_confusion(X_test, y_test)
    
    # 6. Guardar resultados
    print("\n[6/7] Guardando resultados...")
    trainer.guardar_resultados(df_resumen)
    
    # 7. Guardar mejor modelo
    print("\n[7/7] Guardando mejor modelo...")
    trainer.guardar_mejor_modelo('best_model.pkl')
    
    print("\n" + "="*100)
    print("✓ ENTRENAMIENTO Y EVALUACIÓN COMPLETADOS")
    print("="*100)
    print("\nArchivos generados:")
    print("  - best_model.pkl")
    print("  - best_model_metadata.json")
    print("  - resultados_modelos.csv")
    print("  - resultados_modelos.json")
    print("  - comparacion_modelos.png")
    print("  - matriz_confusion.png")
    print("\nPróximo paso: Model Deployment (model_deploy.py)")


if __name__ == "__main__":
    main()
