"""
Model Monitoring - MLOps Project

Este módulo implementa el monitoreo de Data Drift para detectar cambios en la distribución
de datos que puedan afectar el rendimiento del modelo.

Características principales:
- Cálculo de múltiples métricas de drift: KS, PSI, Jensen-Shannon, Chi-cuadrado
- Detección de drift para variables numéricas y categóricas
- Sistema de alertas basado en umbrales
- Generación de reportes y visualizaciones
- Soporte para monitoreo periódico

Autor: MLOps Pipeline
Fecha: 2025
"""

import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Estadística
from scipy import stats
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp, chi2_contingency

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns


class DataDriftMonitor:
    """
    Monitor de Data Drift para detección de cambios en distribución de datos.
    """
    
    def __init__(self, project_root: Path):
        """
        Inicializa el monitor de drift.
        
        Parámetros:
        -----------
        project_root : Path
            Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / 'mlops_pipeline' / 'data'
        self.monitoring_dir = self.project_root / 'mlops_pipeline' / 'monitoring'
        self.reports_dir = self.project_root / 'mlops_pipeline' / 'reports'
        
        # Crear directorios
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Umbrales de drift
        self.umbrales = {
            'ks_statistic': 0.1,      # Kolmogorov-Smirnov
            'psi': 0.2,                # Population Stability Index
            'jensen_shannon': 0.1,     # Jensen-Shannon Divergence
            'chi_square_pvalue': 0.05  # Chi-cuadrado (p-value)
        }
        
        self.resultados_drift = {}
    
    @staticmethod
    def convert_to_serializable(obj):
        """Convierte tipos NumPy a tipos serializables en JSON."""
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: DataDriftMonitor.convert_to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [DataDriftMonitor.convert_to_serializable(item) for item in obj]
        return obj
        
    def cargar_datos_referencia(self, archivo: str = 'datasets_procesados.pkl') -> pd.DataFrame:
        """
        Carga los datos de referencia (entrenamiento).
        
        Parámetros:
        -----------
        archivo : str
            Nombre del archivo
            
        Retorna:
        --------
        pd.DataFrame : DataFrame de referencia
        """
        ruta = self.data_dir / 'processed' / archivo
        
        with open(ruta, 'rb') as f:
            datasets = pickle.load(f)
        
        # Convertir a DataFrame si es array
        X_train = datasets['X_train']
        if isinstance(X_train, np.ndarray):
            # Intentar cargar nombres de features
            try:
                feature_names_path = self.project_root / 'mlops_pipeline' / 'models' / 'feature_names.json'
                with open(feature_names_path, 'r') as f:
                    feature_names = json.load(f)
                X_train = pd.DataFrame(X_train, columns=feature_names)
            except:
                X_train = pd.DataFrame(X_train)
        
        print(f"✓ Datos de referencia cargados: {X_train.shape}")
        return X_train
    
    def simular_datos_actuales(self, 
                               df_referencia: pd.DataFrame, 
                               drift_factor: float = 0.1,
                               n_samples: int = None) -> pd.DataFrame:
        """
        Simula datos actuales añadiendo drift artificial para demostración.
        
        Parámetros:
        -----------
        df_referencia : pd.DataFrame
            Datos de referencia
        drift_factor : float
            Factor de drift a introducir (0-1)
        n_samples : int, opcional
            Número de muestras a simular
            
        Retorna:
        --------
        pd.DataFrame : Datos actuales simulados
        """
        if n_samples is None:
            n_samples = len(df_referencia)
        
        # Muestrear datos de referencia
        df_actual = df_referencia.sample(n=min(n_samples, len(df_referencia)), 
                                         random_state=42).copy()
        
        # Introducir drift en algunas columnas
        for col in df_actual.columns[:int(len(df_actual.columns) * 0.3)]:  # 30% de columnas
            if df_actual[col].dtype in ['float64', 'int64']:
                # Añadir ruido y cambio de media
                ruido = np.random.normal(0, df_actual[col].std() * drift_factor, len(df_actual))
                cambio_media = df_actual[col].mean() * drift_factor
                df_actual[col] = df_actual[col] + ruido + cambio_media
        
        print(f"✓ Datos actuales simulados: {df_actual.shape}")
        print(f"  Drift factor aplicado: {drift_factor}")
        
        return df_actual
    
    def calcular_ks_statistic(self, 
                             ref_data: np.ndarray, 
                             curr_data: np.ndarray) -> Tuple[float, float]:
        """
        Calcula el estadístico de Kolmogorov-Smirnov.
        
        Parámetros:
        -----------
        ref_data : np.ndarray
            Datos de referencia
        curr_data : np.ndarray
            Datos actuales
            
        Retorna:
        --------
        tuple : (estadístico, p-value)
        """
        statistic, pvalue = ks_2samp(ref_data, curr_data)
        return statistic, pvalue
    
    def calcular_psi(self, 
                    ref_data: np.ndarray, 
                    curr_data: np.ndarray, 
                    n_bins: int = 10) -> float:
        """
        Calcula el Population Stability Index (PSI).
        
        Parámetros:
        -----------
        ref_data : np.ndarray
            Datos de referencia
        curr_data : np.ndarray
            Datos actuales
        n_bins : int
            Número de bins para discretizar
            
        Retorna:
        --------
        float : Valor PSI
        """
        # Crear bins basados en datos de referencia
        bins = np.percentile(ref_data, np.linspace(0, 100, n_bins + 1))
        bins = np.unique(bins)  # Eliminar duplicados
        
        if len(bins) < 2:
            return 0.0
        
        # Histogramas
        ref_hist, _ = np.histogram(ref_data, bins=bins)
        curr_hist, _ = np.histogram(curr_data, bins=bins)
        
        # Normalizar
        ref_prop = ref_hist / len(ref_data)
        curr_prop = curr_hist / len(curr_data)
        
        # Evitar división por cero
        ref_prop = np.where(ref_prop == 0, 0.0001, ref_prop)
        curr_prop = np.where(curr_prop == 0, 0.0001, curr_prop)
        
        # Calcular PSI
        psi = np.sum((curr_prop - ref_prop) * np.log(curr_prop / ref_prop))
        
        return psi
    
    def calcular_jensen_shannon(self, 
                               ref_data: np.ndarray, 
                               curr_data: np.ndarray,
                               n_bins: int = 10) -> float:
        """
        Calcula la divergencia de Jensen-Shannon.
        
        Parámetros:
        -----------
        ref_data : np.ndarray
            Datos de referencia
        curr_data : np.ndarray
            Datos actuales
        n_bins : int
            Número de bins
            
        Retorna:
        --------
        float : Divergencia JS
        """
        # Crear bins
        bins = np.linspace(
            min(ref_data.min(), curr_data.min()),
            max(ref_data.max(), curr_data.max()),
            n_bins + 1
        )
        
        # Histogramas normalizados
        ref_hist, _ = np.histogram(ref_data, bins=bins, density=True)
        curr_hist, _ = np.histogram(curr_data, bins=bins, density=True)
        
        # Normalizar para que sumen 1
        ref_hist = ref_hist / ref_hist.sum()
        curr_hist = curr_hist / curr_hist.sum()
        
        # Calcular JS
        js_distance = jensenshannon(ref_hist, curr_hist)
        
        return js_distance
    
    def calcular_chi_cuadrado(self, 
                             ref_data: pd.Series, 
                             curr_data: pd.Series) -> Tuple[float, float]:
        """
        Calcula el test de Chi-cuadrado para variables categóricas.
        
        Parámetros:
        -----------
        ref_data : pd.Series
            Datos de referencia
        curr_data : pd.Series
            Datos actuales
            
        Retorna:
        --------
        tuple : (estadístico, p-value)
        """
        # Obtener todas las categorías únicas
        categorias = list(set(ref_data.unique()) | set(curr_data.unique()))
        
        # Crear tabla de contingencia
        ref_counts = ref_data.value_counts().reindex(categorias, fill_value=0)
        curr_counts = curr_data.value_counts().reindex(categorias, fill_value=0)
        
        # Crear tabla
        tabla = pd.DataFrame({
            'Reference': ref_counts.values,
            'Current': curr_counts.values
        })
        
        # Calcular chi-cuadrado
        chi2, pvalue, dof, expected = chi2_contingency(tabla.T)
        
        return chi2, pvalue
    
    def detectar_drift_numerica(self, 
                                ref_data: pd.Series, 
                                curr_data: pd.Series,
                                nombre_variable: str) -> Dict:
        """
        Detecta drift en una variable numérica.
        
        Parámetros:
        -----------
        ref_data : pd.Series
            Datos de referencia
        curr_data : pd.Series
            Datos actuales
        nombre_variable : str
            Nombre de la variable
            
        Retorna:
        --------
        dict : Resultados del análisis de drift
        """
        # Limpiar NaN
        ref_clean = ref_data.dropna()
        curr_clean = curr_data.dropna()
        
        # Calcular métricas
        ks_stat, ks_pvalue = self.calcular_ks_statistic(ref_clean.values, curr_clean.values)
        psi = self.calcular_psi(ref_clean.values, curr_clean.values)
        js_divergence = self.calcular_jensen_shannon(ref_clean.values, curr_clean.values)
        
        # Detectar drift
        drift_detectado = (
            ks_stat > self.umbrales['ks_statistic'] or
            psi > self.umbrales['psi'] or
            js_divergence > self.umbrales['jensen_shannon']
        )
        
        resultado = {
            'variable': nombre_variable,
            'tipo': 'numerica',
            'drift_detectado': drift_detectado,
            'metricas': {
                'ks_statistic': float(ks_stat),
                'ks_pvalue': float(ks_pvalue),
                'psi': float(psi),
                'jensen_shannon': float(js_divergence)
            },
            'estadisticas': {
                'ref_mean': float(ref_clean.mean()),
                'curr_mean': float(curr_clean.mean()),
                'ref_std': float(ref_clean.std()),
                'curr_std': float(curr_clean.std()),
                'cambio_media': float(abs(curr_clean.mean() - ref_clean.mean()) / ref_clean.mean() * 100)
            },
            'severidad': self._calcular_severidad(ks_stat, psi, js_divergence)
        }
        
        return resultado
    
    def detectar_drift_categorica(self, 
                                  ref_data: pd.Series, 
                                  curr_data: pd.Series,
                                  nombre_variable: str) -> Dict:
        """
        Detecta drift en una variable categórica.
        
        Parámetros:
        -----------
        ref_data : pd.Series
            Datos de referencia
        curr_data : pd.Series
            Datos actuales
        nombre_variable : str
            Nombre de la variable
            
        Retorna:
        --------
        dict : Resultados del análisis de drift
        """
        # Limpiar NaN
        ref_clean = ref_data.dropna()
        curr_clean = curr_data.dropna()
        
        # Calcular chi-cuadrado
        chi2_stat, chi2_pvalue = self.calcular_chi_cuadrado(ref_clean, curr_clean)
        
        # Detectar drift
        drift_detectado = chi2_pvalue < self.umbrales['chi_square_pvalue']
        
        # Distribuciones
        ref_dist = ref_clean.value_counts(normalize=True).to_dict()
        curr_dist = curr_clean.value_counts(normalize=True).to_dict()
        
        resultado = {
            'variable': nombre_variable,
            'tipo': 'categorica',
            'drift_detectado': drift_detectado,
            'metricas': {
                'chi_square_statistic': float(chi2_stat),
                'chi_square_pvalue': float(chi2_pvalue)
            },
            'distribuciones': {
                'referencia': {k: float(v) for k, v in list(ref_dist.items())[:10]},
                'actual': {k: float(v) for k, v in list(curr_dist.items())[:10]}
            },
            'severidad': 'alta' if chi2_pvalue < 0.01 else 'media' if chi2_pvalue < 0.05 else 'baja'
        }
        
        return resultado
    
    def _calcular_severidad(self, ks_stat: float, psi: float, js: float) -> str:
        """Calcula la severidad del drift."""
        score = 0
        if ks_stat > self.umbrales['ks_statistic'] * 2:
            score += 3
        elif ks_stat > self.umbrales['ks_statistic']:
            score += 1
        
        if psi > self.umbrales['psi'] * 2:
            score += 3
        elif psi > self.umbrales['psi']:
            score += 1
        
        if js > self.umbrales['jensen_shannon'] * 2:
            score += 3
        elif js > self.umbrales['jensen_shannon']:
            score += 1
        
        if score >= 6:
            return 'critica'
        elif score >= 3:
            return 'alta'
        elif score >= 1:
            return 'media'
        else:
            return 'baja'
    
    def monitorear_dataset(self, 
                          df_referencia: pd.DataFrame, 
                          df_actual: pd.DataFrame) -> Dict:
        """
        Monitorea drift en todo el dataset.
        
        Parámetros:
        -----------
        df_referencia : pd.DataFrame
            Datos de referencia
        df_actual : pd.DataFrame
            Datos actuales
            
        Retorna:
        --------
        dict : Resultados completos del monitoreo
        """
        print("\n" + "="*80)
        print("MONITOREO DE DATA DRIFT")
        print("="*80)
        
        resultados = {
            'timestamp': datetime.now().isoformat(),
            'variables_analizadas': 0,
            'drift_detectado_total': 0,
            'resultados_por_variable': []
        }
        
        # Analizar cada columna
        for col in df_referencia.columns:
            if col not in df_actual.columns:
                continue
            
            print(f"\nAnalizando: {col}")
            
            # Determinar si es numérica o categórica
            if df_referencia[col].dtype in ['float64', 'int64']:
                resultado = self.detectar_drift_numerica(
                    df_referencia[col], df_actual[col], col
                )
            else:
                resultado = self.detectar_drift_categorica(
                    df_referencia[col], df_actual[col], col
                )
            
            resultados['resultados_por_variable'].append(resultado)
            resultados['variables_analizadas'] += 1
            
            if resultado['drift_detectado']:
                resultados['drift_detectado_total'] += 1
                print(f"  ⚠ DRIFT DETECTADO - Severidad: {resultado['severidad']}")
            else:
                print(f"  ✓ Sin drift detectado")
        
        self.resultados_drift = resultados
        return resultados
    
    def generar_alertas(self) -> List[Dict]:
        """
        Genera alertas basadas en los resultados del monitoreo.
        
        Retorna:
        --------
        list : Lista de alertas
        """
        if not self.resultados_drift:
            return []
        
        alertas = []
        
        for resultado in self.resultados_drift['resultados_por_variable']:
            if resultado['drift_detectado']:
                alerta = {
                    'variable': resultado['variable'],
                    'severidad': resultado['severidad'],
                    'tipo': resultado['tipo'],
                    'timestamp': self.resultados_drift['timestamp'],
                    'recomendacion': self._generar_recomendacion(resultado)
                }
                alertas.append(alerta)
        
        return alertas
    
    def _generar_recomendacion(self, resultado: Dict) -> str:
        """Genera recomendaciones basadas en el resultado del drift."""
        severidad = resultado['severidad']
        variable = resultado['variable']
        
        recomendaciones = {
            'critica': f"ACCIÓN URGENTE: Reentrenar el modelo. La variable '{variable}' muestra drift crítico.",
            'alta': f"ATENCIÓN: Revisar la variable '{variable}'. Considerar reentrenamiento del modelo.",
            'media': f"MONITOREAR: La variable '{variable}' muestra cambios. Continuar vigilancia.",
            'baja': f"INFORMATIVO: Cambios menores en '{variable}'. No se requiere acción inmediata."
        }
        
        return recomendaciones.get(severidad, "Sin recomendación específica")
    
    def visualizar_drift(self, df_referencia: pd.DataFrame, df_actual: pd.DataFrame):
        """
        Genera visualizaciones de drift.
        
        Parámetros:
        -----------
        df_referencia : pd.DataFrame
            Datos de referencia
        df_actual : pd.DataFrame
            Datos actuales
        """
        if not self.resultados_drift:
            print("⚠ Ejecuta monitorear_dataset() primero")
            return
        
        # Filtrar variables con drift
        variables_con_drift = [
            r for r in self.resultados_drift['resultados_por_variable']
            if r['drift_detectado']
        ]
        
        if not variables_con_drift:
            print("✓ No hay drift para visualizar")
            return
        
        # Crear gráficos
        n_vars = min(6, len(variables_con_drift))  # Máximo 6 variables
        n_cols = 2
        n_rows = (n_vars + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        if isinstance(axes, np.ndarray):
            axes = axes.flatten()
        else:
            axes = [axes]
        
        for idx, resultado in enumerate(variables_con_drift[:n_vars]):
            var = resultado['variable']
            ax = axes[idx]
            
            if resultado['tipo'] == 'numerica':
                # Histogramas superpuestos
                ax.hist(df_referencia[var].dropna(), bins=30, alpha=0.5, 
                       label='Referencia', density=True, edgecolor='black')
                ax.hist(df_actual[var].dropna(), bins=30, alpha=0.5, 
                       label='Actual', density=True, edgecolor='black')
                ax.set_xlabel(var)
                ax.set_ylabel('Densidad')
            else:
                # Gráficos de barras para categóricas
                ref_counts = df_referencia[var].value_counts().head(10)
                curr_counts = df_actual[var].value_counts().head(10)
                
                x = np.arange(len(ref_counts))
                width = 0.35
                
                ax.bar(x - width/2, ref_counts.values, width, label='Referencia', alpha=0.8)
                ax.bar(x + width/2, curr_counts.values, width, label='Actual', alpha=0.8)
                ax.set_xlabel(var)
                ax.set_ylabel('Frecuencia')
                ax.set_xticks(x)
                ax.set_xticklabels(ref_counts.index, rotation=45, ha='right')
            
            ax.set_title(f"{var}\nSeveridad: {resultado['severidad']}", fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # Ocultar ejes vacíos
        for idx in range(n_vars, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        # Guardar
        ruta_fig = self.reports_dir / 'drift_visualization.png'
        plt.savefig(ruta_fig, dpi=300, bbox_inches='tight')
        print(f"✓ Visualización guardada en: {ruta_fig}")
        
        plt.show()
    
    def guardar_resultados(self):
        """Guarda los resultados del monitoreo."""
        if not self.resultados_drift:
            print("⚠ No hay resultados para guardar")
            return
        
        # Convertir resultados a tipos serializables
        resultados_serializables = self.convert_to_serializable(self.resultados_drift)
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_json = self.monitoring_dir / f'drift_report_{timestamp}.json'
        
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(resultados_serializables, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Resultados guardados en: {ruta_json}")
        
        # Guardar alertas
        alertas = self.generar_alertas()
        if alertas:
            alertas_serializables = self.convert_to_serializable(alertas)
            ruta_alertas = self.monitoring_dir / f'alertas_{timestamp}.json'
            with open(ruta_alertas, 'w', encoding='utf-8') as f:
                json.dump(alertas_serializables, f, indent=2, ensure_ascii=False)
            print(f"✓ Alertas guardadas en: {ruta_alertas}")
    
    def generar_reporte(self):
        """Genera un reporte resumido del monitoreo."""
        if not self.resultados_drift:
            print("⚠ No hay resultados para reportar")
            return
        
        print("\n" + "="*80)
        print("REPORTE DE MONITOREO DE DRIFT")
        print("="*80)
        print(f"\nFecha: {self.resultados_drift['timestamp']}")
        print(f"Variables analizadas: {self.resultados_drift['variables_analizadas']}")
        print(f"Variables con drift: {self.resultados_drift['drift_detectado_total']}")
        
        # Resumen por severidad
        severidades = {}
        for resultado in self.resultados_drift['resultados_por_variable']:
            if resultado['drift_detectado']:
                sev = resultado['severidad']
                severidades[sev] = severidades.get(sev, 0) + 1
        
        if severidades:
            print(f"\nDistribución por severidad:")
            for sev in ['critica', 'alta', 'media', 'baja']:
                if sev in severidades:
                    print(f"  - {sev.capitalize()}: {severidades[sev]}")
        
        # Alertas
        alertas = self.generar_alertas()
        if alertas:
            print(f"\n{'='*80}")
            print("ALERTAS Y RECOMENDACIONES")
            print("="*80)
            for alerta in alertas:
                print(f"\n[{alerta['severidad'].upper()}] {alerta['variable']}")
                print(f"  → {alerta['recomendacion']}")


def main():
    """
    Función principal para ejecutar el monitoreo de drift.
    """
    print("="*80)
    print("MODEL MONITORING - DATA DRIFT DETECTION")
    print("="*80)
    
    # Configuración
    project_root = Path(__file__).parent.parent.parent
    
    # Inicializar monitor
    monitor = DataDriftMonitor(project_root)
    
    # 1. Cargar datos de referencia
    print("\n[1/5] Cargando datos de referencia...")
    df_referencia = monitor.cargar_datos_referencia()
    
    # 2. Simular/cargar datos actuales
    print("\n[2/5] Generando datos actuales (simulación)...")
    df_actual = monitor.simular_datos_actuales(df_referencia, drift_factor=0.15)
    
    # 3. Monitorear drift
    print("\n[3/5] Monitoreando drift...")
    resultados = monitor.monitorear_dataset(df_referencia, df_actual)
    
    # 4. Visualizar
    print("\n[4/5] Generando visualizaciones...")
    monitor.visualizar_drift(df_referencia, df_actual)
    
    # 5. Guardar y reportar
    print("\n[5/5] Guardando resultados...")
    monitor.guardar_resultados()
    monitor.generar_reporte()
    
    print("\n" + "="*80)
    print("✓ MONITOREO COMPLETADO")
    print("="*80)
    print("\nPróximo paso: Crear aplicación Streamlit para visualización")


if __name__ == "__main__":
    main()
