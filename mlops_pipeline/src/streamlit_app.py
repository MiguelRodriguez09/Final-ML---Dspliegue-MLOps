"""
Streamlit App para Visualización de Monitoreo de Modelos.

Esta aplicación proporciona una interfaz web para:
    - Visualizar métricas de drift
    - Mostrar alertas
    - Generar recomendaciones
    - Ejecutar análisis de drift en tiempo real
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurar la ruta del proyecto correctamente
# De streamlit_app.py -> src -> mlops_pipeline -> Proyecto (raíz)
project_root = Path(__file__).resolve().parent.parent.parent

# Agregar al path de Python si no está
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importar el DriftMonitor
from mlops_pipeline.src.model_monitoring import DriftMonitor


# Configuración de la página
st.set_page_config(
    page_title="MLOps Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .alert-moderate {
        background-color: #fff9c4;
        border-left: 5px solid #ffc107;
    }
    .alert-low {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)


def load_drift_report():
    """Carga el reporte de drift más reciente."""
    report_path = project_root / 'data' / 'metadata' / 'drift_report.json'
    
    # Debug: Mostrar la ruta que se está buscando
    print(f"DEBUG: Buscando drift_report.json en: {report_path}")
    print(f"DEBUG: Archivo existe: {report_path.exists()}")
    
    if report_path.exists():
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"DEBUG: drift_report.json cargado exitosamente")
                return data
        except Exception as e:
            print(f"ERROR: No se pudo cargar drift_report.json: {e}")
            return None
    else:
        print(f"WARNING: drift_report.json no encontrado en {report_path}")
        return None


def load_model_metadata():
    """Carga los metadatos del modelo."""
    metadata_path = project_root / 'models' / 'model_metadata.json'
    
    # Debug: Mostrar la ruta que se está buscando
    print(f"DEBUG: Buscando model_metadata.json en: {metadata_path}")
    print(f"DEBUG: Archivo existe: {metadata_path.exists()}")
    
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"DEBUG: model_metadata.json cargado exitosamente")
                return data
        except Exception as e:
            print(f"ERROR: No se pudo cargar model_metadata.json: {e}")
            return None
    else:
        print(f"WARNING: model_metadata.json no encontrado en {metadata_path}")
        return None


def display_summary_metrics(drift_report):
    """Muestra métricas de resumen."""
    st.markdown('<p class="main-header">📊 MLOps Monitoring Dashboard</p>', 
                unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Columnas Analizadas",
            value=drift_report['summary']['total_columns']
        )
    
    with col2:
        st.metric(
            label="Drift Detectado",
            value=drift_report['summary']['columns_with_drift'],
            delta=f"{drift_report['summary']['drift_percentage']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Sin Drift",
            value=drift_report['summary']['columns_no_drift']
        )
    
    with col4:
        # Determinar estado general
        drift_pct = drift_report['summary']['drift_percentage']
        if drift_pct < 20:
            status = "🟢 Saludable"
        elif drift_pct < 40:
            status = "🟡 Atención"
        else:
            status = "🔴 Crítico"
        
        st.metric(
            label="Estado del Sistema",
            value=status
        )


def plot_drift_overview(drift_report):
    """Visualiza resumen de drift."""
    st.subheader("📈 Resumen de Drift")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pastel
        labels = ['Con Drift', 'Sin Drift']
        values = [
            drift_report['summary']['columns_with_drift'],
            drift_report['summary']['columns_no_drift']
        ]
        colors = ['#ff6b6b', '#51cf66']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4
        )])
        fig.update_layout(
            title="Distribución de Drift",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de severidad
        severities = {'low': 0, 'moderate': 0, 'high': 0}
        for col_info in drift_report['columns_analyzed']:
            severities[col_info['severity']] += 1
        
        severity_df = pd.DataFrame({
            'Severidad': ['Bajo', 'Moderado', 'Alto'],
            'Cantidad': [severities['low'], severities['moderate'], severities['high']],
            'Color': ['#51cf66', '#ffd43b', '#ff6b6b']
        })
        
        fig = px.bar(
            severity_df,
            x='Severidad',
            y='Cantidad',
            color='Severidad',
            color_discrete_map={
                'Bajo': '#51cf66',
                'Moderado': '#ffd43b',
                'Alto': '#ff6b6b'
            },
            title="Severidad del Drift"
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def plot_psi_metrics(drift_report):
    """Visualiza métricas PSI."""
    st.subheader("📊 Population Stability Index (PSI)")
    
    # Filtrar variables numéricas
    numerical_cols = [c for c in drift_report['columns_analyzed'] 
                     if c['type'] == 'numerical']
    
    if not numerical_cols:
        st.info("No hay variables numéricas para mostrar")
        return
    
    # Crear DataFrame (manejar drift_detected como string o bool)
    def is_drift_detected(col):
        drift = col['drift_detected']
        if isinstance(drift, str):
            return drift.lower() == 'true'
        return bool(drift)
    
    psi_data = pd.DataFrame({
        'Variable': [c['column'] for c in numerical_cols],
        'PSI': [c['psi'] for c in numerical_cols],
        'Drift': ['Sí' if is_drift_detected(c) else 'No' for c in numerical_cols]
    })
    
    psi_data = psi_data.sort_values('PSI', ascending=True)
    
    # Gráfico de barras horizontal
    fig = px.bar(
        psi_data,
        y='Variable',
        x='PSI',
        color='Drift',
        color_discrete_map={'Sí': '#ff6b6b', 'No': '#51cf66'},
        orientation='h',
        title='PSI por Variable'
    )
    
    # Agregar línea de umbral
    fig.add_vline(x=0.2, line_dash="dash", line_color="orange",
                  annotation_text="Umbral (0.2)")
    
    fig.update_layout(height=max(400, len(psi_data) * 30))
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    with st.expander("📋 Ver Detalles"):
        st.dataframe(psi_data, use_container_width=True)


def display_alerts(drift_report):
    """Muestra alertas de drift."""
    st.subheader("🚨 Alertas y Recomendaciones")
    
    # Función auxiliar para manejar drift_detected
    def is_drift_detected(col):
        drift = col['drift_detected']
        if isinstance(drift, str):
            return drift.lower() == 'true'
        return bool(drift)
    
    # Generar alertas
    alerts = []
    
    for col_info in drift_report['columns_analyzed']:
        if is_drift_detected(col_info):
            severity_class = f"alert-{col_info['severity']}"
            
            if col_info['type'] == 'numerical':
                alert_text = (
                    f"**{col_info['column']}** - Drift {col_info['severity'].upper()}\n\n"
                    f"- PSI: {col_info['psi']:.3f}\n"
                    f"- Media Referencia: {col_info['reference_mean']:.2f}\n"
                    f"- Media Actual: {col_info['current_mean']:.2f}\n"
                    f"- Desviación: {col_info['mean_shift']:.2f} std"
                )
            else:
                alert_text = (
                    f"**{col_info['column']}** - Drift {col_info['severity'].upper()}\n\n"
                    f"- Chi² p-value: {col_info['chi2_pvalue']:.4f}\n"
                    f"- Cambio en distribución categórica detectado"
                )
            
            alerts.append((severity_class, alert_text, col_info['severity']))
    
    # Ordenar por severidad
    severity_order = {'high': 0, 'moderate': 1, 'low': 2}
    alerts.sort(key=lambda x: severity_order[x[2]])
    
    if alerts:
        for severity_class, alert_text, _ in alerts:
            st.markdown(
                f'<div class="alert-box {severity_class}">{alert_text}</div>',
                unsafe_allow_html=True
            )
    else:
        st.success("✅ No se detectaron alertas. El sistema está funcionando correctamente.")
    
    # Recomendaciones
    st.markdown("---")
    st.markdown("### 💡 Recomendaciones")
    
    drift_pct = drift_report['summary']['drift_percentage']
    
    if drift_pct > 30:
        st.error(
            "🔴 **Acción Requerida:** Se recomienda reentrenar el modelo debido a "
            "drift significativo en más del 30% de las variables."
        )
    elif drift_pct > 15:
        st.warning(
            "🟡 **Monitoreo Cercano:** Aumentar la frecuencia de monitoreo y "
            "considerar reentrenamiento si el drift continúa aumentando."
        )
    else:
        st.success(
            "🟢 **Estado Normal:** El drift está dentro de rangos aceptables. "
            "Continuar con el monitoreo regular."
        )


def display_detailed_analysis(drift_report):
    """Muestra análisis detallado por variable."""
    st.subheader("🔍 Análisis Detallado por Variable")
    
    # Selector de variable
    variables = [c['column'] for c in drift_report['columns_analyzed']]
    selected_var = st.selectbox("Seleccionar Variable:", variables)
    
    # Obtener información de la variable
    var_info = next(c for c in drift_report['columns_analyzed'] 
                   if c['column'] == selected_var)
    
    # Mostrar información
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Información General")
        st.write(f"**Tipo:** {var_info['type']}")
        st.write(f"**Severidad:** {var_info['severity'].upper()}")
        st.write(f"**Drift Detectado:** {'Sí' if var_info['drift_detected'] else 'No'}")
    
    with col2:
        st.markdown("#### Métricas")
        if var_info['type'] == 'numerical':
            st.write(f"**PSI:** {var_info['psi']:.4f}")
            st.write(f"**KS Statistic:** {var_info['ks_statistic']:.4f}")
            st.write(f"**KS p-value:** {var_info['ks_pvalue']:.4f}")
        else:
            st.write(f"**Chi² Statistic:** {var_info['chi2']:.4f}")
            st.write(f"**Chi² p-value:** {var_info['chi2_pvalue']:.4f}")
    
    # Comparación de distribuciones
    if var_info['type'] == 'numerical':
        st.markdown("#### Estadísticas Descriptivas")
        
        comparison_df = pd.DataFrame({
            'Métrica': ['Media', 'Desviación Estándar'],
            'Referencia': [var_info['reference_mean'], var_info['reference_std']],
            'Actual': [var_info['current_mean'], var_info['current_std']]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
    else:
        st.markdown("#### Distribución Categórica")
        
        ref_dist = pd.DataFrame(list(var_info['reference_distribution'].items()),
                               columns=['Categoría', 'Frecuencia Referencia'])
        curr_dist = pd.DataFrame(list(var_info['current_distribution'].items()),
                                columns=['Categoría', 'Frecuencia Actual'])
        
        dist_df = pd.merge(ref_dist, curr_dist, on='Categoría', how='outer').fillna(0)
        st.dataframe(dist_df, use_container_width=True)


def display_model_info():
    """Muestra información del modelo en el sidebar."""
    st.sidebar.title("ℹ️ Información del Modelo")
    
    model_metadata = load_model_metadata()
    
    if model_metadata:
        st.sidebar.markdown(f"**Modelo:** {model_metadata.get('model_name', 'N/A')}")
        st.sidebar.markdown(f"**Tipo:** {model_metadata.get('model_type', 'N/A')}")
        
        metrics = model_metadata.get('metrics', {})
        if metrics:
            st.sidebar.markdown("### Métricas del Modelo")
            st.sidebar.metric("Test Accuracy", f"{metrics.get('test_accuracy', 0):.3f}")
            st.sidebar.metric("Test F1-Score", f"{metrics.get('test_f1', 0):.3f}")
            st.sidebar.metric("Test ROC-AUC", f"{metrics.get('test_roc_auc', 0):.3f}")
    else:
        st.sidebar.info("Metadatos del modelo no disponibles")


def main():
    """Función principal de la aplicación Streamlit."""
    
    # Debug: Mostrar información del proyecto
    print("="*80)
    print("DEBUG: Información de Rutas")
    print("="*80)
    print(f"project_root: {project_root}")
    print(f"project_root existe: {project_root.exists()}")
    print(f"__file__: {__file__}")
    print("="*80)
    
    # Sidebar
    display_model_info()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Acciones")
    
    if st.sidebar.button("🔄 Actualizar Análisis", use_container_width=True):
        with st.spinner("Ejecutando análisis de drift..."):
            try:
                monitor = DriftMonitor(project_root, alert_threshold=0.2)
                monitor.load_reference_data()
                
                current_data_path = project_root / 'test_data.csv'
                current_data = pd.read_csv(current_data_path)
                
                # Analizar drift y guardar reporte
                monitor.analyze_drift(current_data)
                monitor.save_drift_report()
                
                st.sidebar.success("✅ Análisis completado")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
    
    # Cargar reporte
    drift_report = load_drift_report()
    
    if drift_report is None:
        st.error("⚠️ **No hay reporte de drift disponible**")
        st.info("""
        **Para generar el reporte de drift, sigue estos pasos:**
        
        1. Asegúrate de haber ejecutado el pipeline completo:
           - `ft_engineering.py` → genera `train_data.csv` y `test_data.csv`
           - `model_training_evaluation.py` → genera `best_model.pkl` y `model_metadata.json`
           - `model_monitoring.py` → genera `drift_report.json`
        
        2. O haz clic en el botón **"🔄 Actualizar Análisis"** en la barra lateral.
        
        3. Verifica que existan los siguientes archivos en la raíz del proyecto:
           - `train_data.csv`
           - `test_data.csv`
           - `model_metadata.json`
        """)
        
        # Mostrar información de debug
        with st.expander("🔍 Información de Debug"):
            st.code(f"""
Ruta del proyecto: {project_root}
Directorio existe: {project_root.exists()}

Archivos esperados:
- drift_report.json: {(project_root / 'drift_report.json').exists()}
- model_metadata.json: {(project_root / 'model_metadata.json').exists()}
- train_data.csv: {(project_root / 'train_data.csv').exists()}
- test_data.csv: {(project_root / 'test_data.csv').exists()}
            """)
        return
    
    # Mostrar timestamp
    st.caption(f"Última actualización: {drift_report.get('timestamp', 'N/A')}")
    
    # Métricas de resumen
    display_summary_metrics(drift_report)
    
    st.markdown("---")
    
    # Tabs para diferentes vistas
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Resumen", "📊 Métricas PSI", "🚨 Alertas", "🔍 Análisis Detallado"]
    )
    
    with tab1:
        plot_drift_overview(drift_report)
    
    with tab2:
        plot_psi_metrics(drift_report)
    
    with tab3:
        display_alerts(drift_report)
    
    with tab4:
        display_detailed_analysis(drift_report)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "MLOps Pipeline - Monitoring Dashboard | Desarrollado con Streamlit"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
