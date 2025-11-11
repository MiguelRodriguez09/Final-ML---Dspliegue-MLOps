"""
Model Training and Evaluation Module para MLOps Pipeline.

Este módulo implementa el entrenamiento, evaluación y selección de modelos
de Machine Learning de forma genérica y reutilizable.

Flujo:
    1. Carga de datos procesados
    2. Entrenamiento de múltiples modelos
    3. Validación cruzada
    4. Evaluación y comparación
    5. Selección del mejor modelo
    6. Guardado del modelo seleccionado
"""

import json
import logging
import warnings
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc
)

warnings.filterwarnings('ignore')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Clase para entrenar y evaluar modelos de Machine Learning.
    
    Attributes:
        project_root: Ruta raíz del proyecto
        models: Diccionario de modelos a entrenar
        results: Resultados de evaluación de modelos
        best_model: Mejor modelo seleccionado
    """
    
    def __init__(self, project_root: Path):
        """
        Inicializa el ModelTrainer.
        
        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.models: Dict[str, Any] = {}
        self.results: Dict[str, Dict[str, float]] = {}
        self.best_model: Optional[Any] = None
        self.best_model_name: str = ""
        logger.info("ModelTrainer inicializado correctamente")
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Carga los datos procesados de entrenamiento y prueba.
        
        Returns:
            Tupla (train_data, test_data)
        """
        train_path = self.project_root / 'data' / 'processed' / 'train_data.csv'
        test_path = self.project_root / 'data' / 'processed' / 'test_data.csv'
        
        if not train_path.exists() or not test_path.exists():
            raise FileNotFoundError("Datos procesados no encontrados. Ejecutar ft_engineering.py primero.")
        
        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)
        
        logger.info(f"Datos cargados - Train: {train_data.shape}, Test: {test_data.shape}")
        return train_data, test_data
    
    def split_features_target(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        target_col: str = 'Exited'
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Separa features y target de los datasets.
        
        Args:
            train_data: Datos de entrenamiento
            test_data: Datos de prueba
            target_col: Nombre de la columna objetivo
        
        Returns:
            Tupla (X_train, X_test, y_train, y_test)
        """
        X_train = train_data.drop(columns=[target_col]).values
        y_train = train_data[target_col].values
        X_test = test_data.drop(columns=[target_col]).values
        y_test = test_data[target_col].values
        
        logger.info(f"Datos separados - X_train: {X_train.shape}, y_train: {y_train.shape}")
        return X_train, X_test, y_train, y_test
    
    def build_models(self) -> Dict[str, Any]:
        """
        Define los modelos a entrenar.
        
        Returns:
            Diccionario de modelos
        """
        models = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=10,
                min_samples_split=20,
                random_state=42
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=20,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        self.models = models
        logger.info(f"{len(models)} modelos configurados")
        return models
    
    def train_and_evaluate_model(
        self,
        model: Any,
        model_name: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        cv_folds: int = 5
    ) -> Dict[str, float]:
        """
        Entrena y evalúa un modelo individual.
        
        Args:
            model: Modelo a entrenar
            model_name: Nombre del modelo
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento
            X_test: Features de prueba
            y_test: Target de prueba
            cv_folds: Número de folds para validación cruzada
        
        Returns:
            Diccionario con métricas de evaluación
        """
        logger.info(f"Entrenando {model_name}...")
        
        # Entrenamiento
        model.fit(X_train, y_train)
        
        # Predicciones
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Probabilidades para ROC-AUC
        if hasattr(model, 'predict_proba'):
            y_train_proba = model.predict_proba(X_train)[:, 1]
            y_test_proba = model.predict_proba(X_test)[:, 1]
        else:
            y_train_proba = y_train_pred
            y_test_proba = y_test_pred
        
        # Validación cruzada
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
        
        # Calcular métricas
        metrics = {
            'train_accuracy': accuracy_score(y_train, y_train_pred),
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'train_precision': precision_score(y_train, y_train_pred, zero_division=0),
            'test_precision': precision_score(y_test, y_test_pred, zero_division=0),
            'train_recall': recall_score(y_train, y_train_pred, zero_division=0),
            'test_recall': recall_score(y_test, y_test_pred, zero_division=0),
            'train_f1': f1_score(y_train, y_train_pred, zero_division=0),
            'test_f1': f1_score(y_test, y_test_pred, zero_division=0),
            'train_roc_auc': roc_auc_score(y_train, y_train_proba),
            'test_roc_auc': roc_auc_score(y_test, y_test_proba),
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        logger.info(f"{model_name} - Test Accuracy: {metrics['test_accuracy']:.4f}, "
                   f"Test F1: {metrics['test_f1']:.4f}")
        
        return metrics
    
    def train_all_models(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, Dict[str, float]]:
        """
        Entrena y evalúa todos los modelos.
        
        Args:
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento
            X_test: Features de prueba
            y_test: Target de prueba
        
        Returns:
            Diccionario con resultados de todos los modelos
        """
        results = {}
        
        for model_name, model in self.models.items():
            metrics = self.train_and_evaluate_model(
                model, model_name, X_train, y_train, X_test, y_test
            )
            results[model_name] = metrics
        
        self.results = results
        return results
    
    def summarize_classification(self, results: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """
        Genera un resumen de las métricas de clasificación.
        
        Args:
            results: Resultados de evaluación de modelos
        
        Returns:
            DataFrame con resumen de métricas
        """
        summary_data = []
        
        for model_name, metrics in results.items():
            summary_data.append({
                'Model': model_name,
                'Train_Accuracy': metrics['train_accuracy'],
                'Test_Accuracy': metrics['test_accuracy'],
                'Test_Precision': metrics['test_precision'],
                'Test_Recall': metrics['test_recall'],
                'Test_F1': metrics['test_f1'],
                'Test_ROC_AUC': metrics['test_roc_auc'],
                'CV_Mean': metrics['cv_mean'],
                'CV_Std': metrics['cv_std'],
                'Overfit': metrics['train_accuracy'] - metrics['test_accuracy']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values('Test_F1', ascending=False)
        
        return summary_df
    
    def plot_model_comparison(self, summary_df: pd.DataFrame) -> None:
        """
        Visualiza la comparación de modelos.
        
        Args:
            summary_df: DataFrame con resumen de métricas
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Gráfico 1: Accuracy comparison
        ax1 = axes[0, 0]
        x_pos = np.arange(len(summary_df))
        width = 0.35
        ax1.bar(x_pos - width/2, summary_df['Train_Accuracy'], 
               width, label='Train', alpha=0.8)
        ax1.bar(x_pos + width/2, summary_df['Test_Accuracy'], 
               width, label='Test', alpha=0.8)
        ax1.set_xlabel('Model')
        ax1.set_ylabel('Accuracy')
        ax1.set_title('Train vs Test Accuracy')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(summary_df['Model'], rotation=45, ha='right')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Gráfico 2: Test Metrics comparison
        ax2 = axes[0, 1]
        metrics_to_plot = ['Test_Precision', 'Test_Recall', 'Test_F1', 'Test_ROC_AUC']
        x_pos = np.arange(len(summary_df))
        width = 0.2
        for i, metric in enumerate(metrics_to_plot):
            ax2.bar(x_pos + i*width, summary_df[metric], 
                   width, label=metric.replace('Test_', ''), alpha=0.8)
        ax2.set_xlabel('Model')
        ax2.set_ylabel('Score')
        ax2.set_title('Test Metrics Comparison')
        ax2.set_xticks(x_pos + width * 1.5)
        ax2.set_xticklabels(summary_df['Model'], rotation=45, ha='right')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # Gráfico 3: Cross-validation scores
        ax3 = axes[1, 0]
        ax3.bar(summary_df['Model'], summary_df['CV_Mean'], 
               yerr=summary_df['CV_Std'], capsize=5, alpha=0.8)
        ax3.set_xlabel('Model')
        ax3.set_ylabel('CV Accuracy')
        ax3.set_title('Cross-Validation Performance')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(axis='y', alpha=0.3)
        
        # Gráfico 4: Overfitting analysis
        ax4 = axes[1, 1]
        colors = ['green' if x < 0.05 else 'orange' if x < 0.1 else 'red' 
                 for x in summary_df['Overfit']]
        ax4.bar(summary_df['Model'], summary_df['Overfit'], 
               color=colors, alpha=0.8)
        ax4.axhline(y=0.05, color='green', linestyle='--', label='Good (<0.05)')
        ax4.axhline(y=0.1, color='orange', linestyle='--', label='Moderate (<0.1)')
        ax4.set_xlabel('Model')
        ax4.set_ylabel('Overfit (Train - Test Accuracy)')
        ax4.set_title('Overfitting Analysis')
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.project_root / 'reports' / 'plots' / 'model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Gráficos de comparación generados")
    
    def plot_confusion_matrices(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> None:
        """
        Genera matrices de confusión para todos los modelos.
        
        Args:
            X_test: Features de prueba
            y_test: Target de prueba
        """
        n_models = len(self.models)
        fig, axes = plt.subplots(1, n_models, figsize=(5*n_models, 4))
        
        if n_models == 1:
            axes = [axes]
        
        for idx, (model_name, model) in enumerate(self.models.items()):
            y_pred = model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       cbar=False, square=True)
            axes[idx].set_title(f'{model_name}')
            axes[idx].set_xlabel('Predicted')
            axes[idx].set_ylabel('Actual')
        
        plt.tight_layout()
        plt.savefig(self.project_root / 'reports' / 'plots' / 'confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Matrices de confusión generadas")
    
    def plot_roc_curves(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> None:
        """
        Genera curvas ROC para todos los modelos.
        
        Args:
            X_test: Features de prueba
            y_test: Target de prueba
        """
        plt.figure(figsize=(10, 8))
        
        for model_name, model in self.models.items():
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_proba)
                roc_auc = auc(fpr, tpr)
                
                plt.plot(fpr, tpr, lw=2, 
                        label=f'{model_name} (AUC = {roc_auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves Comparison')
        plt.legend(loc='lower right')
        plt.grid(alpha=0.3)
        
        plt.savefig(self.project_root / 'reports' / 'plots' / 'roc_curves.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Curvas ROC generadas")
    
    def select_best_model(
        self,
        summary_df: pd.DataFrame,
        metric: str = 'Test_F1'
    ) -> Tuple[Any, str]:
        """
        Selecciona el mejor modelo basado en una métrica.
        
        Args:
            summary_df: DataFrame con resumen de métricas
            metric: Métrica para selección
        
        Returns:
            Tupla (mejor_modelo, nombre_modelo)
        """
        best_model_name = summary_df.iloc[0]['Model']
        best_model = self.models[best_model_name]
        
        self.best_model = best_model
        self.best_model_name = best_model_name
        
        logger.info(f"Mejor modelo seleccionado: {best_model_name} "
                   f"({metric} = {summary_df.iloc[0][metric]:.4f})")
        
        return best_model, best_model_name
    
    def save_best_model(self) -> None:
        """
        Guarda el mejor modelo y sus metadatos.
        """
        if self.best_model is None:
            raise ValueError("No hay modelo seleccionado. Ejecutar select_best_model() primero.")
        
        # Guardar modelo
        model_path = self.project_root / 'models' / 'best_model.pkl'
        joblib.dump(self.best_model, model_path)
        logger.info(f"Modelo guardado en: {model_path}")
        
        # Guardar metadatos
        metadata = {
            'model_name': self.best_model_name,
            'model_type': str(type(self.best_model).__name__),
            'metrics': self.results[self.best_model_name],
            'all_results': self.results
        }
        
        metadata_path = self.project_root / 'models' / 'model_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadatos guardados en: {metadata_path}")


def main() -> None:
    """
    Función principal para ejecutar el entrenamiento y evaluación de modelos.
    """
    # Configurar rutas
    project_root = Path(__file__).parent.parent.parent
    
    print("="*70)
    print("MODEL TRAINING & EVALUATION - MLOps Pipeline")
    print("="*70)
    
    # Inicializar ModelTrainer
    trainer = ModelTrainer(project_root)
    
    # 1. Cargar datos
    print("\n[1/8] Cargando datos procesados...")
    train_data, test_data = trainer.load_data()
    print(f"✓ Datos cargados")
    
    # 2. Separar features y target
    print("\n[2/8] Separando features y target...")
    X_train, X_test, y_train, y_test = trainer.split_features_target(train_data, test_data)
    print(f"✓ Datos separados")
    
    # 3. Construir modelos
    print("\n[3/8] Construyendo modelos...")
    models = trainer.build_models()
    print(f"✓ {len(models)} modelos configurados")
    
    # 4. Entrenar y evaluar modelos
    print("\n[4/8] Entrenando y evaluando modelos...")
    results = trainer.train_all_models(X_train, y_train, X_test, y_test)
    print(f"✓ Modelos entrenados")
    
    # 5. Generar resumen
    print("\n[5/8] Generando resumen de resultados...")
    summary_df = trainer.summarize_classification(results)
    print("\nRESUMEN DE MODELOS:\n")
    print(summary_df.to_string(index=False))
    
    # 6. Visualizaciones
    print("\n[6/8] Generando visualizaciones...")
    trainer.plot_model_comparison(summary_df)
    trainer.plot_confusion_matrices(X_test, y_test)
    trainer.plot_roc_curves(X_test, y_test)
    print("✓ Visualizaciones generadas")
    
    # 7. Seleccionar mejor modelo
    print("\n[7/8] Seleccionando mejor modelo...")
    best_model, best_model_name = trainer.select_best_model(summary_df)
    print(f"✓ Mejor modelo: {best_model_name}")
    
    # 8. Guardar mejor modelo
    print("\n[8/8] Guardando mejor modelo...")
    trainer.save_best_model()
    print("✓ Modelo guardado")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE ENTRENAMIENTO")
    print("="*70)
    print(f"Modelos evaluados: {len(models)}")
    print(f"Mejor modelo: {best_model_name}")
    print(f"Test F1-Score: {results[best_model_name]['test_f1']:.4f}")
    print(f"Test ROC-AUC: {results[best_model_name]['test_roc_auc']:.4f}")
    print("\n✓ ENTRENAMIENTO COMPLETADO")
    print("→ Continuar con model_deploy.py")
    print("="*70)


if __name__ == "__main__":
    main()
