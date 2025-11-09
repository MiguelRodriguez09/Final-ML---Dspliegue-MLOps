"""
Model Monitoring Module para MLOps Pipeline.

Este módulo implementa el monitoreo de data drift y genera alertas
cuando se detectan desviaciones significativas en los datos.

Funcionalidades:
    - Detección de Data Drift (Kolmogorov-Smirnov, PSI, Chi-cuadrado)
    - Cálculo de métricas de drift
    - Generación de alertas
    - Visualización de drift
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ks_2samp, chi2_contingency

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DriftMonitor:
    """
    Clase para monitorear data drift en datos de producción.
    
    Attributes:
        project_root: Ruta raíz del proyecto
        reference_data: Datos de referencia (entrenamiento)
        drift_results: Resultados de análisis de drift
        alert_threshold: Umbral para alertas (PSI)
    """
    
    def __init__(self, project_root: Path, alert_threshold: float = 0.2):
        """
        Inicializa el DriftMonitor.
        
        Args:
            project_root: Ruta raíz del proyecto
            alert_threshold: Umbral de PSI para generar alertas
        """
        self.project_root = Path(project_root)
        self.reference_data: Optional[pd.DataFrame] = None
        self.drift_results: Dict[str, Any] = {}
        self.alert_threshold = alert_threshold
        logger.info("DriftMonitor inicializado correctamente")
    
    def load_reference_data(self) -> pd.DataFrame:
        """
        Carga los datos de referencia (training data).
        
        Returns:
            DataFrame de referencia
        """
        train_path = self.project_root / 'train_data.csv'
        
        if not train_path.exists():
            raise FileNotFoundError(f"No se encontró {train_path}")
        
        self.reference_data = pd.read_csv(train_path)
        logger.info(f"Datos de referencia cargados: {self.reference_data.shape}")
        return self.reference_data
    
    def calculate_psi(
        self,
        reference: np.ndarray,
        current: np.ndarray,
        n_bins: int = 10
    ) -> float:
        """
        Calcula el Population Stability Index (PSI).
        
        Args:
            reference: Datos de referencia
            current: Datos actuales
            n_bins: Número de bins para discretización
        
        Returns:
            Valor de PSI
        """
        # Eliminar nulos
        reference = reference[~np.isnan(reference)]
        current = current[~np.isnan(current)]
        
        if len(reference) == 0 or len(current) == 0:
            return 0.0
        
        # Crear bins basados en datos de referencia
        bins = np.linspace(reference.min(), reference.max(), n_bins + 1)
        bins[0] = -np.inf
        bins[-1] = np.inf
        
        # Calcular distribuciones
        ref_dist = np.histogram(reference, bins=bins)[0] / len(reference)
        curr_dist = np.histogram(current, bins=bins)[0] / len(current)
        
        # Agregar pequeño valor para evitar log(0)
        ref_dist = ref_dist + 1e-10
        curr_dist = curr_dist + 1e-10
        
        # Calcular PSI
        psi = np.sum((curr_dist - ref_dist) * np.log(curr_dist / ref_dist))
        
        return psi
    
    def calculate_ks_statistic(
        self,
        reference: np.ndarray,
        current: np.ndarray
    ) -> Tuple[float, float]:
        """
        Calcula la estadística de Kolmogorov-Smirnov.
        
        Args:
            reference: Datos de referencia
            current: Datos actuales
        
        Returns:
            Tupla (estadística KS, p-value)
        """
        # Eliminar nulos
        reference = reference[~np.isnan(reference)]
        current = current[~np.isnan(current)]
        
        if len(reference) == 0 or len(current) == 0:
            return 0.0, 1.0
        
        ks_stat, p_value = ks_2samp(reference, current)
        return ks_stat, p_value
    
    def calculate_chi_square(
        self,
        reference: pd.Series,
        current: pd.Series
    ) -> Tuple[float, float]:
        """
        Calcula el test Chi-cuadrado para variables categóricas.
        
        Args:
            reference: Datos de referencia
            current: Datos actuales
        
        Returns:
            Tupla (chi2, p-value)
        """
        # Crear tabla de contingencia
        ref_counts = reference.value_counts()
        curr_counts = current.value_counts()
        
        # Unir índices
        all_categories = set(ref_counts.index) | set(curr_counts.index)
        
        ref_freq = [ref_counts.get(cat, 0) for cat in all_categories]
        curr_freq = [curr_counts.get(cat, 0) for cat in all_categories]
        
        # Crear tabla de contingencia
        contingency_table = np.array([ref_freq, curr_freq])
        
        # Chi-cuadrado
        try:
            chi2, p_value, _, _ = chi2_contingency(contingency_table)
            return chi2, p_value
        except ValueError:
            return 0.0, 1.0
    
    def detect_drift_numerical(
        self,
        column: str,
        reference: pd.Series,
        current: pd.Series
    ) -> Dict[str, Any]:
        """
        Detecta drift en variable numérica.
        
        Args:
            column: Nombre de la columna
            reference: Datos de referencia
            current: Datos actuales
        
        Returns:
            Diccionario con métricas de drift
        """
        # PSI
        psi = self.calculate_psi(reference.values, current.values)
        
        # KS Test
        ks_stat, ks_pvalue = self.calculate_ks_statistic(reference.values, current.values)
        
        # Estadísticas descriptivas
        ref_mean = reference.mean()
        curr_mean = current.mean()
        ref_std = reference.std()
        curr_std = current.std()
        
        # Determinar severidad del drift
        if psi < 0.1:
            severity = "low"
        elif psi < 0.2:
            severity = "moderate"
        else:
            severity = "high"
        
        drift_info = {
            'column': column,
            'type': 'numerical',
            'psi': psi,
            'ks_statistic': ks_stat,
            'ks_pvalue': ks_pvalue,
            'reference_mean': ref_mean,
            'current_mean': curr_mean,
            'reference_std': ref_std,
            'current_std': curr_std,
            'mean_shift': abs(curr_mean - ref_mean) / ref_std if ref_std > 0 else 0,
            'severity': severity,
            'drift_detected': psi > self.alert_threshold
        }
        
        logger.info(f"{column} - PSI: {psi:.4f}, Severity: {severity}")
        return drift_info
    
    def detect_drift_categorical(
        self,
        column: str,
        reference: pd.Series,
        current: pd.Series
    ) -> Dict[str, Any]:
        """
        Detecta drift en variable categórica.
        
        Args:
            column: Nombre de la columna
            reference: Datos de referencia
            current: Datos actuales
        
        Returns:
            Diccionario con métricas de drift
        """
        # Chi-cuadrado
        chi2, chi2_pvalue = self.calculate_chi_square(reference, current)
        
        # Distribuciones
        ref_dist = reference.value_counts(normalize=True)
        curr_dist = current.value_counts(normalize=True)
        
        # Determinar severidad
        severity = "low" if chi2_pvalue > 0.05 else "moderate" if chi2_pvalue > 0.01 else "high"
        
        drift_info = {
            'column': column,
            'type': 'categorical',
            'chi2': chi2,
            'chi2_pvalue': chi2_pvalue,
            'reference_distribution': ref_dist.to_dict(),
            'current_distribution': curr_dist.to_dict(),
            'severity': severity,
            'drift_detected': chi2_pvalue < 0.05
        }
        
        logger.info(f"{column} - Chi2 p-value: {chi2_pvalue:.4f}, Severity: {severity}")
        return drift_info
    
    def analyze_drift(
        self,
        current_data: pd.DataFrame,
        target_col: str = 'Exited'
    ) -> Dict[str, Any]:
        """
        Analiza drift en todos las columnas.
        
        Args:
            current_data: Datos actuales a comparar
            target_col: Columna objetivo (excluir del análisis)
        
        Returns:
            Diccionario con resultados de drift
        """
        if self.reference_data is None:
            self.load_reference_data()
        
        drift_results = {
            'timestamp': datetime.now().isoformat(),
            'n_samples_reference': len(self.reference_data),
            'n_samples_current': len(current_data),
            'columns_analyzed': [],
            'drift_detected': [],
            'no_drift': [],
            'summary': {}
        }
        
        # Analizar cada columna
        for col in self.reference_data.columns:
            if col == target_col:
                continue
            
            if col not in current_data.columns:
                logger.warning(f"Columna {col} no encontrada en datos actuales")
                continue
            
            # Determinar tipo de variable
            if self.reference_data[col].dtype in ['int64', 'float64']:
                # Variable numérica
                drift_info = self.detect_drift_numerical(
                    col,
                    self.reference_data[col],
                    current_data[col]
                )
            else:
                # Variable categórica
                drift_info = self.detect_drift_categorical(
                    col,
                    self.reference_data[col],
                    current_data[col]
                )
            
            drift_results['columns_analyzed'].append(drift_info)
            
            if drift_info['drift_detected']:
                drift_results['drift_detected'].append(col)
            else:
                drift_results['no_drift'].append(col)
        
        # Resumen
        drift_results['summary'] = {
            'total_columns': len(drift_results['columns_analyzed']),
            'columns_with_drift': len(drift_results['drift_detected']),
            'columns_no_drift': len(drift_results['no_drift']),
            'drift_percentage': (len(drift_results['drift_detected']) / 
                               len(drift_results['columns_analyzed']) * 100) 
                               if drift_results['columns_analyzed'] else 0
        }
        
        self.drift_results = drift_results
        logger.info(f"Análisis de drift completado: {drift_results['summary']['columns_with_drift']}"
                   f"/{drift_results['summary']['total_columns']} columnas con drift")
        
        return drift_results
    
    def generate_alerts(self) -> List[str]:
        """
        Genera alertas basadas en el análisis de drift.
        
        Returns:
            Lista de mensajes de alerta
        """
        if not self.drift_results:
            logger.warning("No hay resultados de drift. Ejecutar analyze_drift() primero.")
            return []
        
        alerts = []
        
        # Alerta general
        if self.drift_results['summary']['columns_with_drift'] > 0:
            alerts.append(
                f"⚠️ ALERTA: Se detectó drift en {self.drift_results['summary']['columns_with_drift']} "
                f"de {self.drift_results['summary']['total_columns']} columnas "
                f"({self.drift_results['summary']['drift_percentage']:.1f}%)"
            )
        
        # Alertas específicas por columna
        for col_info in self.drift_results['columns_analyzed']:
            if col_info['drift_detected'] and col_info['severity'] in ['moderate', 'high']:
                if col_info['type'] == 'numerical':
                    alerts.append(
                        f"🔴 {col_info['column']}: Drift {col_info['severity']} "
                        f"(PSI={col_info['psi']:.3f})"
                    )
                else:
                    alerts.append(
                        f"🔴 {col_info['column']}: Drift {col_info['severity']} "
                        f"(Chi2 p-value={col_info['chi2_pvalue']:.3f})"
                    )
        
        # Recomendaciones
        if self.drift_results['summary']['drift_percentage'] > 30:
            alerts.append(
                "💡 RECOMENDACIÓN: Considerar reentrenamiento del modelo debido a drift significativo"
            )
        
        return alerts
    
    def plot_drift_summary(self) -> None:
        """
        Visualiza un resumen del análisis de drift.
        """
        if not self.drift_results:
            logger.warning("No hay resultados para visualizar")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Resumen general
        ax1 = axes[0, 0]
        categories = ['Con Drift', 'Sin Drift']
        values = [
            self.drift_results['summary']['columns_with_drift'],
            self.drift_results['summary']['columns_no_drift']
        ]
        colors = ['#ff6b6b', '#51cf66']
        ax1.pie(values, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Resumen de Drift', fontweight='bold')
        
        # 2. PSI por columna (numéricas)
        ax2 = axes[0, 1]
        numerical_cols = [c for c in self.drift_results['columns_analyzed'] 
                         if c['type'] == 'numerical']
        if numerical_cols:
            col_names = [c['column'] for c in numerical_cols]
            psi_values = [c['psi'] for c in numerical_cols]
            colors_psi = ['red' if psi > self.alert_threshold else 'green' 
                         for psi in psi_values]
            
            ax2.barh(col_names, psi_values, color=colors_psi, alpha=0.7)
            ax2.axvline(x=self.alert_threshold, color='orange', linestyle='--', 
                       label=f'Threshold ({self.alert_threshold})')
            ax2.set_xlabel('PSI')
            ax2.set_title('PSI - Variables Numéricas', fontweight='bold')
            ax2.legend()
        else:
            ax2.text(0.5, 0.5, 'No hay variables numéricas', 
                    ha='center', va='center', transform=ax2.transAxes)
        
        # 3. Severidad del drift
        ax3 = axes[1, 0]
        severities = {'low': 0, 'moderate': 0, 'high': 0}
        for col_info in self.drift_results['columns_analyzed']:
            severities[col_info['severity']] += 1
        
        severity_labels = list(severities.keys())
        severity_values = list(severities.values())
        severity_colors = ['#51cf66', '#ffd43b', '#ff6b6b']
        
        ax3.bar(severity_labels, severity_values, color=severity_colors, alpha=0.7, edgecolor='black')
        ax3.set_ylabel('Número de Columnas')
        ax3.set_title('Severidad del Drift', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Timeline (placeholder para monitoreo continuo)
        ax4 = axes[1, 1]
        ax4.text(0.5, 0.5, 
                f"Análisis: {self.drift_results['timestamp']}\n\n"
                f"Muestras Referencia: {self.drift_results['n_samples_reference']:,}\n"
                f"Muestras Actuales: {self.drift_results['n_samples_current']:,}",
                ha='center', va='center', transform=ax4.transAxes,
                fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax4.axis('off')
        ax4.set_title('Información del Análisis', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.project_root / 'drift_summary.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Visualización de drift generada")
    
    def save_drift_report(self) -> None:
        """
        Guarda el reporte de drift en JSON.
        """
        if not self.drift_results:
            logger.warning("No hay resultados para guardar")
            return
        
        report_path = self.project_root / 'drift_report.json'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.drift_results, f, indent=2, default=str)
        
        logger.info(f"Reporte de drift guardado en: {report_path}")


def main() -> None:
    """
    Función principal para ejecutar el monitoreo de drift.
    """
    # Configurar rutas
    project_root = Path(__file__).parent.parent.parent
    
    print("="*70)
    print("MODEL MONITORING - Data Drift Detection")
    print("="*70)
    
    # Inicializar monitor
    monitor = DriftMonitor(project_root, alert_threshold=0.2)
    
    # 1. Cargar datos de referencia
    print("\n[1/5] Cargando datos de referencia...")
    monitor.load_reference_data()
    print("✓ Datos de referencia cargados")
    
    # 2. Simular datos actuales (usar test data como ejemplo)
    print("\n[2/5] Cargando datos actuales...")
    current_data_path = project_root / 'test_data.csv'
    current_data = pd.read_csv(current_data_path)
    print(f"✓ Datos actuales cargados: {current_data.shape}")
    
    # 3. Analizar drift
    print("\n[3/5] Analizando drift...")
    drift_results = monitor.analyze_drift(current_data)
    print("✓ Análisis completado")
    
    # 4. Generar alertas
    print("\n[4/5] Generando alertas...")
    alerts = monitor.generate_alerts()
    if alerts:
        print("\nALERTAS DETECTADAS:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("✓ No se detectaron alertas críticas")
    
    # 5. Visualizar y guardar
    print("\n[5/5] Generando visualizaciones y reportes...")
    monitor.plot_drift_summary()
    monitor.save_drift_report()
    print("✓ Reportes generados")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE MONITOREO")
    print("="*70)
    print(f"Columnas analizadas: {drift_results['summary']['total_columns']}")
    print(f"Drift detectado: {drift_results['summary']['columns_with_drift']} columnas")
    print(f"Porcentaje de drift: {drift_results['summary']['drift_percentage']:.1f}%")
    print("\n✓ MONITOREO COMPLETADO")
    print("="*70)


if __name__ == "__main__":
    main()
