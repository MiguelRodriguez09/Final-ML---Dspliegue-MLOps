"""
Aplicación Streamlit para Monitoreo de MLOps

Esta aplicación web proporciona una interfaz interactiva para:
- Visualizar métricas de drift
- Comparar distribuciones históricas vs actuales
- Mostrar alertas y recomendaciones
- Evolución temporal del drift

Autor: MLOps Pipeline
Fecha: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys

# Añadir el directorio del proyecto al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Importar módulos del proyecto
from mlops_pipeline.src.model_monitoring import DataDriftMonitor


# Configuración de la página
st.set_page_config(
    page_title="MLOps Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border-left: 5px solid #1f77b4;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .alert-high {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .alert-medium {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos_monitor():
    """Carga los datos del monitor."""
    monitor = DataDriftMonitor(project_root)
    df_ref = monitor.cargar_datos_referencia()
    df_curr = monitor.simular_datos_actuales(df_ref, drift_factor=0.15)
    return monitor, df_ref, df_curr


@st.cache_data
def cargar_resultados_drift(_monitor, df_ref, df_curr):
    """Carga o genera resultados de drift."""
    resultados = _monitor.monitorear_dataset(df_ref, df_curr)
    return resultados


def mostrar_metricas_principales(resultados):
    """Muestra las métricas principales en tarjetas."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Variables Analizadas",
            value=resultados['variables_analizadas'],
            delta=None
        )
    
    with col2:
        drift_detectado = resultados['drift_detectado_total']
        st.metric(
            label="Drift Detectado",
            value=drift_detectado,
            delta=f"{(drift_detectado/resultados['variables_analizadas']*100):.1f}%",
            delta_color="inverse"
        )
    
    # Contar por severidad
    severidades = {}
    for r in resultados['resultados_por_variable']:
        if r['drift_detectado']:
            sev = r['severidad']
            severidades[sev] = severidades.get(sev, 0) + 1
    
    with col3:
        criticas = severidades.get('critica', 0) + severidades.get('alta', 0)
        st.metric(
            label="Alertas Críticas/Altas",
            value=criticas,
            delta_color="inverse"
        )
    
    with col4:
        timestamp = datetime.fromisoformat(resultados['timestamp'])
        tiempo_desde = datetime.now() - timestamp
        st.metric(
            label="Última Actualización",
            value=f"{tiempo_desde.seconds // 60} min",
            delta=None
        )


def mostrar_semaforo_drift(resultados):
    """Muestra un indicador de semáforo para el estado del drift."""
    drift_total = resultados['drift_detectado_total']
    total_vars = resultados['variables_analizadas']
    porcentaje_drift = (drift_total / total_vars * 100) if total_vars > 0 else 0
    
    # Determinar color del semáforo
    if porcentaje_drift > 30:
        color = "🔴"
        estado = "CRÍTICO"
        mensaje = "Se requiere acción inmediata. Reentrenamiento del modelo recomendado."
    elif porcentaje_drift > 15:
        color = "🟡"
        estado = "ADVERTENCIA"
        mensaje = "Monitorear de cerca. Considerar revisión del modelo."
    else:
        color = "🟢"
        estado = "NORMAL"
        mensaje = "Sistema operando dentro de parámetros normales."
    
    st.markdown(f"### {color} Estado del Sistema: {estado}")
    st.info(mensaje)
    
    # Barra de progreso
    st.progress(min(porcentaje_drift / 100, 1.0))


def mostrar_alertas(resultados):
    """Muestra las alertas generadas."""
    st.header("🚨 Alertas y Recomendaciones")
    
    variables_con_drift = [
        r for r in resultados['resultados_por_variable']
        if r['drift_detectado']
    ]
    
    if not variables_con_drift:
        st.success("✅ No hay alertas activas. El sistema está funcionando correctamente.")
        return
    
    # Ordenar por severidad
    orden_severidad = {'critica': 0, 'alta': 1, 'media': 2, 'baja': 3}
    variables_con_drift.sort(key=lambda x: orden_severidad.get(x['severidad'], 99))
    
    for var_result in variables_con_drift:
        severidad = var_result['severidad']
        variable = var_result['variable']
        
        # Seleccionar estilo según severidad
        if severidad == 'critica':
            icon = "🔴"
            class_name = "alert-critical"
        elif severidad == 'alta':
            icon = "🟠"
            class_name = "alert-high"
        else:
            icon = "🔵"
            class_name = "alert-medium"
        
        # Generar recomendación
        if severidad in ['critica', 'alta']:
            recomendacion = f"ACCIÓN REQUERIDA: Revisar la variable '{variable}' y considerar reentrenamiento del modelo."
        elif severidad == 'media':
            recomendacion = f"MONITOREAR: Continuar vigilancia de la variable '{variable}'."
        else:
            recomendacion = f"INFORMATIVO: Cambios menores detectados en '{variable}'."
        
        st.markdown(f"""
        <div class="{class_name}">
            <h4>{icon} {variable.upper()} - Severidad: {severidad.capitalize()}</h4>
            <p><strong>Recomendación:</strong> {recomendacion}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar métricas específicas
        with st.expander(f"Ver detalles de {variable}"):
            metricas = var_result.get('metricas', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.json(metricas)
            
            with col2:
                if 'estadisticas' in var_result:
                    st.write("**Estadísticas:**")
                    st.json(var_result['estadisticas'])


def mostrar_comparacion_distribuciones(resultados, df_ref, df_curr):
    """Muestra comparación de distribuciones."""
    st.header("📊 Comparación de Distribuciones")
    
    # Seleccionar variable
    variables = [r['variable'] for r in resultados['resultados_por_variable']]
    variable_seleccionada = st.selectbox(
        "Selecciona una variable para comparar:",
        variables
    )
    
    # Obtener resultado de la variable
    resultado_var = next(
        (r for r in resultados['resultados_por_variable'] 
         if r['variable'] == variable_seleccionada),
        None
    )
    
    if resultado_var is None:
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de distribución
        if resultado_var['tipo'] == 'numerica':
            fig = go.Figure()
            
            # Histograma de referencia
            fig.add_trace(go.Histogram(
                x=df_ref[variable_seleccionada].dropna(),
                name='Referencia',
                opacity=0.6,
                nbinsx=30,
                histnorm='probability density'
            ))
            
            # Histograma actual
            fig.add_trace(go.Histogram(
                x=df_curr[variable_seleccionada].dropna(),
                name='Actual',
                opacity=0.6,
                nbinsx=30,
                histnorm='probability density'
            ))
            
            fig.update_layout(
                title=f"Distribución de {variable_seleccionada}",
                xaxis_title=variable_seleccionada,
                yaxis_title="Densidad",
                barmode='overlay',
                height=400
            )
            
        else:  # Categórica
            ref_counts = df_ref[variable_seleccionada].value_counts().head(10)
            curr_counts = df_curr[variable_seleccionada].value_counts().head(10)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=ref_counts.index,
                y=ref_counts.values,
                name='Referencia',
                opacity=0.8
            ))
            fig.add_trace(go.Bar(
                x=curr_counts.index,
                y=curr_counts.values,
                name='Actual',
                opacity=0.8
            ))
            
            fig.update_layout(
                title=f"Distribución de {variable_seleccionada}",
                xaxis_title=variable_seleccionada,
                yaxis_title="Frecuencia",
                barmode='group',
                height=400
            )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Métricas de drift
        st.markdown("### Métricas de Drift")
        
        if resultado_var['drift_detectado']:
            st.error("⚠️ Drift Detectado")
        else:
            st.success("✅ Sin Drift")
        
        st.markdown(f"**Severidad:** {resultado_var['severidad'].capitalize()}")
        
        st.markdown("### Valores de Métricas")
        metricas = resultado_var['metricas']
        for metrica, valor in metricas.items():
            st.metric(label=metrica, value=f"{valor:.4f}")


def mostrar_evolucion_temporal():
    """Muestra la evolución temporal del drift (simulada)."""
    st.header("📈 Evolución Temporal del Drift")
    
    # Simular datos históricos
    n_periodos = 30
    fechas = [datetime.now() - timedelta(days=i) for i in range(n_periodos, 0, -1)]
    
    # Simular métricas que aumentan gradualmente
    drift_porcentaje = [
        5 + i * 0.5 + np.random.normal(0, 2)
        for i in range(n_periodos)
    ]
    
    df_temporal = pd.DataFrame({
        'Fecha': fechas,
        'Drift (%)': drift_porcentaje
    })
    
    # Gráfico
    fig = px.line(
        df_temporal,
        x='Fecha',
        y='Drift (%)',
        title='Evolución del Drift a lo Largo del Tiempo',
        markers=True
    )
    
    # Añadir líneas de umbral
    fig.add_hline(y=15, line_dash="dash", line_color="orange", 
                  annotation_text="Umbral Advertencia")
    fig.add_hline(y=30, line_dash="dash", line_color="red", 
                  annotation_text="Umbral Crítico")
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Función principal de la aplicación."""
    # Header
    st.markdown('<h1 class="main-header">📊 MLOps Monitoring Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50.png?text=MLOps", width=150)
        st.title("Configuración")
        
        st.markdown("### Umbrales de Drift")
        umbral_ks = st.slider("KS Statistic", 0.0, 1.0, 0.1, 0.01)
        umbral_psi = st.slider("PSI", 0.0, 1.0, 0.2, 0.01)
        
        st.markdown("---")
        st.markdown("### Acciones")
        if st.button("🔄 Actualizar Datos"):
            st.cache_data.clear()
            st.rerun()
        
        if st.button("📥 Descargar Reporte"):
            st.info("Funcionalidad en desarrollo")
        
        st.markdown("---")
        st.markdown("### Información")
        st.info("Dashboard de monitoreo en tiempo real para detección de drift de datos.")
    
    # Cargar datos
    with st.spinner("Cargando datos del monitor..."):
        monitor, df_ref, df_curr = cargar_datos_monitor()
        resultados = cargar_resultados_drift(monitor, df_ref, df_curr)
    
    # Actualizar umbrales si cambiaron
    monitor.umbrales['ks_statistic'] = umbral_ks
    monitor.umbrales['psi'] = umbral_psi
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🚨 Alertas", 
        "📈 Distribuciones", 
        "⏱️ Evolución Temporal"
    ])
    
    with tab1:
        # Métricas principales
        mostrar_metricas_principales(resultados)
        st.markdown("---")
        
        # Semáforo
        col1, col2 = st.columns([1, 2])
        with col1:
            mostrar_semaforo_drift(resultados)
        
        with col2:
            # Tabla resumen
            st.markdown("### Resumen de Variables con Drift")
            drift_vars = [
                {
                    'Variable': r['variable'],
                    'Tipo': r['tipo'],
                    'Severidad': r['severidad'],
                    'Drift': '✅' if not r['drift_detectado'] else '⚠️'
                }
                for r in resultados['resultados_por_variable']
                if r['drift_detectado']
            ]
            
            if drift_vars:
                df_drift = pd.DataFrame(drift_vars)
                st.dataframe(df_drift, use_container_width=True)
            else:
                st.success("No hay variables con drift detectado")
    
    with tab2:
        mostrar_alertas(resultados)
    
    with tab3:
        mostrar_comparacion_distribuciones(resultados, df_ref, df_curr)
    
    with tab4:
        mostrar_evolucion_temporal()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "MLOps Pipeline © 2025 | Última actualización: " + 
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
