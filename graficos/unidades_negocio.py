import polars as pl
import plotly.express as px

from utils.funciones_ayuda import formatear_valor

def obtener_ingresos_unidad_negocio(datos):
    datos_unidad_negocio = datos.filter(pl.col("Clasificación1")=="Estado Resultados")
    datos_unidad_negocio = datos_unidad_negocio.select(["Unidad de negocio","Neto","mes","mes_numero"])
    datos_unidad_negocio = datos_unidad_negocio.group_by(["Unidad de negocio","mes","mes_numero"]
                                                              ).agg(pl.col("Neto").sum()
                                                              ).with_columns((pl.col("Neto") * -1).alias("Neto")
                                                                ).sort(["mes_numero"])
    return datos_unidad_negocio

def tabla_unidad_negocio(datos):
    datos = obtener_ingresos_unidad_negocio(datos)
    datos_tabla = datos.pivot("Unidad de negocio",index="mes",values="Neto")

    #obtenemos el total
    fila_total = pl.DataFrame({
    "mes": ["total"],
    **{col: [datos_tabla[col].sum()] for col in datos_tabla.columns 
       if col != "mes" }})
    datos_tabla = pl.concat([datos_tabla, fila_total])

    datos_tabla = datos_tabla.with_columns([
        pl.col(c).map_elements(formatear_valor).alias(c)
    for c in datos_tabla.columns if c != "mes"])
    
    return datos_tabla

def grafico_barras_ingresos_por_unidad_negocio(datos):
    datos_unidad_negocio = obtener_ingresos_unidad_negocio(datos)
    #datos_unidad_negocio = datos_unidad_negocio.pivot("mes",index="Unidad de negocio",values="Neto",)
    fig = px.bar(
    datos_unidad_negocio.select(["Unidad de negocio","mes","Neto"]).to_dict(as_series=False),  # convierte Polars → dict (Plotly lo entiende bien)
    x="mes",
    y="Neto",
    color="Unidad de negocio",
    barmode="group",
    title="Ingresos por Unidad de Negocio y Mes",
   
    )

    fig.update_traces(
    texttemplate='%{text:,.0f}',     # formato de texto
    textposition='inside'       
)

    # Mejora la presentación
    fig.update_layout(
        title={
        "text": "Ingresos por Unidad de Negocio y Mes",
        "y": 0.95,                 # ajusta la posición vertical del título (por defecto 0.9)
        "x": 0.5,                  # centrado horizontal
        "xanchor": "center",
        "yanchor": "top",
        "pad": {"b": 30}           # 🔹 agrega 30px de espacio debajo del título
        },
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_title="Mes",
        yaxis_title="Valor Neto",
        template="plotly_white",
         legend=dict(
        orientation="h",  
        yanchor="bottom",
        y=1.02, 
        xanchor="center",
        x=0.5     ))

    return fig