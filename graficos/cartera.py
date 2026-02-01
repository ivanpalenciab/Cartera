import polars as pl
import plotly.express as px
import pandas as pd

def grafico_deuda_cliente(datos):
    datos["Cliente corto"] = datos["Cliente"].str.slice(0, 20) + "..."

    fig = px.bar(
        datos[["Cliente corto","Total cartera"]],
        y="Cliente corto",
        x="Total cartera",
        #orientation="h",
        title = "Deuda por cliente"
    )

    fig.update_layout(
        margin=dict(l=250),
        template="plotly_white"   # aumenta este valor si aún queda apretado
    )

    return fig

def grafico_deuda_cliente_estado(datos):
    datos["Cliente corto"] = datos["Cliente"].str.slice(0, 20) + "..."
    fig = px.bar(
        datos[["Cliente corto","Total cartera","estado"]],
        x="Total cartera",
        y="Cliente corto",
        color="estado",
        barmode="group",
        title="Deuda por cliente y estado"

    )

    return fig
    

def porcentaje_deuda_cliente(datos):
    """Esta funcion me proporcionara los 7 clientes que mas deuda acumulan"""
    #tota_cartera = datos["Total cartera"].sum()

    deuda_cliente = datos.groupby("Cliente",as_index=False
                                   ).agg({"Total cartera":"sum"})
    #deuda_cliente["porcentaje"] = deuda_cliente["Total cartera"]/tota_cartera

    #sacamos el top 7 de las empresas con mas deuda
    deuda_ordenada = deuda_cliente.sort_values(by='Total cartera',ascending=False)
    top_7 = deuda_ordenada.head(7)

    #sacamos el resto
    otros = deuda_ordenada.iloc[7:]
    otros_sumado = otros["Total cartera"].sum()
    fila_otros = pd.DataFrame([{"Cliente": "Otros", "Total cartera": otros_sumado}])

    deuda_mostrar = pd.concat([top_7, fila_otros], ignore_index=True)
    

    #deuda_mostrar = deuda_cliente.head(7)

    fig = px.pie(deuda_mostrar, values='Total cartera', names='Cliente', title='Porcentaje deuda por cliente')
    print(deuda_mostrar)

    return fig

def porcentaje_deuda_duracion():
    """Esta funcion genera un diagrama de pastel con el porcentaje de deuda
    por una categoria de acuerdo a la duración de la deuda"""