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
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
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
        #hover_data={'Total cartera': ':,.2f'}, # Formato con comas y 2 decimales
        color="estado",
        barmode="group",
        title="Deuda por cliente y estado"

    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=250),
        template="plotly_white"   # aumenta este valor si aún queda apretado
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

    fig = px.pie(deuda_mostrar, values='Total cartera', names='Cliente', title='Porcentaje deuda por cliente')
    print(deuda_mostrar)

    return fig

def porcentaje_deuda_duracion(datos):
    """Esta funcion genera un diagrama de pastel con el porcentaje de deuda
    por una categoria de acuerdo a la duración de la deuda"""
    pass

def deuda_cliente_por_duracion_deuda(datos):
    """ Esta funcion genera un diagrama con la deuda de cliente por la duración
    de la deuda"""

    datos["Cliente corto"] = datos["Cliente"].str.slice(0, 20) + "..."

    datos["duracion_deuda"] = pd.cut(
        datos["vencimiento"],
        bins=[-float('inf'),-180,-90,-1,float('inf')],
        labels=[
            "mayor a 6 meses","entre 3 y 6 meses"," menor a 3 meses","al dia"
        ]
    )
    #datos_agrupado = datos[["Cliente","duracion_deuda","Total cartera"]].groupby(["Cliente","duracion_deuda"]).sum()
    #datos.to_excel('archivo.xlsx', index=False)

    print("Estos son los datos que quiero revisar")
    #print(datos[["Cliente",'Fecha vencimiento',"vencimiento","duracion_deuda"]])
    fig = px.bar(
        datos[["Cliente corto","Total cartera","duracion_deuda"]],
        x="Total cartera",
        y="Cliente corto",
        #hover_data={'Total cartera': ':,.2f'}, # Formato con comas y 2 decimales
        color="duracion_deuda",
        barmode="group",
        title="Deuda por cliente y duración deuda"

    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=250),
        template="plotly_white"   # aumenta este valor si aún queda apretado
    )
    return fig