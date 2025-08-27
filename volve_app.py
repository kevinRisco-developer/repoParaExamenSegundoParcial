# volve_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Historial de Producción - Campo Volve", layout="wide")

st.title("Historial de Producción del Campo Volve")

st.markdown("""
El campo **Volve**, ubicado en el Mar del Norte, fue operado por Equinor y produjo
petróleo y gas durante los años 2008 - 2016. En este período, se registró la producción
de hidrocarburos y agua en varios pozos, lo que constituye un caso de estudio muy
utilizado en la industria petrolera y académica.
""")

st.image("img/pozo.jpg", use_column_width=True) 

@st.cache_data
def load_data():
    df = pd.read_excel("volve_params.xlsx")
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    return df

df = load_data()
df["Year"] = pd.to_datetime(df["DATEPRD"]).dt.year
df = df.rename(columns={
    "BORE_OIL_VOL": "Vol_o",
    "BORE_GAS_VOL": "Vol_g",
    "BORE_WAT_VOL": "Vol_w",
    "NPD_WELL_BORE_NAME": "Well"
})
menu = st.sidebar.radio("Menú", ["Home", "Data", "Plots"])

if menu == "Home":
    st.subheader("Bienvenido")
    st.write("""
    En esta aplicación podrá explorar los datos históricos de producción del **Campo Volve**.
    Se incluyen volúmenes de petróleo, gas y agua, junto con visualizaciones que permiten
    analizar el comportamiento de los pozos en el tiempo.
    """)

elif menu == "Data":
    st.subheader("Datos de Producción")
    st.write("El siguiente dataframe contiene los registros históricos de producción por pozo y año.")
    st.dataframe(df)

elif menu == "Plots":
    st.subheader("Visualizaciones de Producción")

    # 1) Vol_o vs t (años)
    st.markdown("**Producción de Petróleo (Vol_o) vs Tiempo (años)**")
    fig1 = px.line(df, x="Year", y="Vol_o", color="Well",
                   title="Vol_o vs Year (por pozo)")
    st.plotly_chart(fig1, use_container_width=True)

    # 2) Vol_g vs t (años)
    st.markdown("**Producción de Gas (Vol_g) vs Tiempo (años)**")
    fig2 = px.line(df, x="Year", y="Vol_g", color="Well",
                   title="Vol_g vs Year (por pozo)")
    st.plotly_chart(fig2, use_container_width=True)

    # 3) Vol_o y Vol_w vs t (años)
    st.markdown("**Producción de Petróleo y Agua vs Tiempo (años)**")
    fig3 = px.line(df, x="Year", y=["Vol_o", "Vol_w"], color="Well",
                   title="Vol_o y Vol_w vs Year (por pozo)")
    st.plotly_chart(fig3, use_container_width=True)

    # 4) Totales por pozo (barras)
    st.markdown("**Totales acumulados por pozo**")
    totals = df.groupby("Well")[["Vol_o", "Vol_g", "Vol_w"]].sum().reset_index()
    fig4 = px.bar(totals, x="Well", y=["Vol_o", "Vol_g", "Vol_w"],
                  barmode="group", title="Totales acumulados por pozo")
    st.plotly_chart(fig4, use_container_width=True)
