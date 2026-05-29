import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Calculadora de Inflación a 30 Años", page_icon="💰", layout="wide")

st.title("💰 Calculadora de Valor Presente Ajustado por Inflación")
st.write("Evalúa el poder adquisitivo real de tu dinero del futuro a precios de hoy.")

# Barra lateral para introducir los datos
st.sidebar.header("Configuración del Cálculo")

monto_futuro = st.sidebar.number_input(
    "Monto futuro a recibir ($):", 
    min_value=0.0, 
    value=16000000.0, 
    step=100000.0,
    format="%.2f"
)

anios = st.sidebar.slider("Plazo en años:", min_value=1, max_value=50, value=30)

st.sidebar.subheader("Tasas de Inflación Anual (%)")
inf_opt = st.sidebar.number_input("Escenario Optimista:", min_value=0.0, max_value=100.0, value=3.5, step=0.1) / 100
inf_mod = st.sidebar.number_input("Escenario Moderado:", min_value=0.0, max_value=100.0, value=4.0, step=0.1) / 100
inf_pes = st.sidebar.number_input("Escenario Pesimista:", min_value=0.0, max_value=100.0, value=4.5, step=0.1) / 100

# Cálculos del Valor Presente
vp_opt = monto_futuro / ((1 + inf_opt) ** anios)
vp_mod = monto_futuro / ((1 + inf_mod) ** anios)
vp_pes = monto_futuro / ((1 + inf_pes) ** anios)

# Sección de Métricas principales
st.subheader(f"Resultados de Equivalencia Actual (en {anios} años)")
col1, col2, col3 = st.columns(3)

col1.metric(label=f"Escenario Optimista ({inf_opt*100:.1f}%)", value=f"${vp_opt:,.2f}")
col2.metric(label=f"Escenario Moderado ({inf_mod*100:.1f}%)", value=f"${vp_mod:,.2f}")
col3.metric(label=f"Escenario Pesimista ({inf_pes*100:.1f}%)", value=f"${vp_pes:,.2f}")

st.markdown("---")

# Generación de datos año con año para la gráfica
lista_anios = np.arange(0, anios + 1)
datos_proyeccion = []

for a in lista_anios:
    datos_proyeccion.append({
        "Año": a,
        "Optimista": monto_futuro / ((1 + inf_opt) ** a),
        "Moderado": monto_futuro / ((1 + inf_mod) ** a),
        "Pesimista": monto_futuro / ((1 + inf_pes) ** a)
    })

df = pd.DataFrame(datos_proyeccion)

# Gráfica interactiva con Plotly
st.subheader("Evolución del Poder Adquisitivo en el Tiempo")
st.write("Esta gráfica muestra cómo disminuye el valor real de tu dinero fijo a medida que pasan los años:")

# Transformar el dataframe para que Plotly Express lo lea correctamente (formato largo)
df_melted = df.melt(id_vars=["Año"], value_vars=["Optimista", "Moderado", "Pesimista"], 
                    var_name="Escenario", value_name="Valor Real ($)")

fig = px.line(
    df_melted, 
    x="Año", 
    y="Valor Real ($)", 
    color="Escenario",
    labels={"Año": "Años transcurridos", "Valor Real ($)": "Poder Adquisitivo ($)"},
    color_discrete_map={"Optimista": "#2ecc71", "Moderado": "#3498db", "Pesimista": "#e74c3c"}
)

fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Tabla de datos para descargar o revisar
with st.expander("Ver tabla de datos detallada año con año"):
    st.dataframe(df.style.format({
        "Optimista": "${:,.2f}",
        "Moderado": "${:,.2f}",
        "Pesimista": "${:,.2f}"
    }))