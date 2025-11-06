from dash import dash_table,dcc
import polars as pl
import plotly.graph_objects as go

from utils.funciones_ayuda import obtener_o_cero
from utils.funciones_ayuda import formatear_valor

def grafico_estado_resultados(datos):
    return dash_table.DataTable(
        id="estado-resultados",
        data=datos.to_dicts(), 
        style_table={'overflowX': 'auto'},
        style_cell={
            "textAlign": "center",
            "fontSize": "9px",
            "padding": "1px 2px",
            "whiteSpace": "nowrap",  # no permite saltos, pero ocupa menos espaci
        },
        )

def grafico_linea_estado_resultados(ingresos_operacionales,costo_ventas,utilidad):
    figura = go.Figure(data=[
        go.Scatter(x=list(utilidad[:, 1:-1].to_dicts()[0].keys()),y=list(utilidad[:, 1:-1].to_dicts()[0].values()),mode="lines",name="Utilidad"),
        go.Scatter(x=list(ingresos_operacionales[:, 1:-1].to_dicts()[0].keys()),y=list(ingresos_operacionales[:, 1:-1].to_dicts()[0].values()),mode="lines",name="Ingreso operacional"),
        go.Scatter(x=list(costo_ventas[:, 1:-1].to_dicts()[0].keys()),y=[-v for v in costo_ventas[:, 1:-1].to_dicts()[0].values()],mode="lines",name="Costo de ventas"),
    ])

    figura.update_layout(
    title="Estado de resultados ",
    xaxis_title="Periodo",
    yaxis_title="Valor",
    title_x=0.5 , # Centra el título
    plot_bgcolor="white",   # fondo del área de trazado
    paper_bgcolor="white", 

    legend=dict(
        orientation="h",  # horizontal
        yanchor="bottom",
        y=1.02,  # posición vertical (un poco encima del gráfico)
        xanchor="center",
        x=0.5     # centrado
    ))

    return figura

def grafico_cascada(datos):
    conceptos_cuentas = datos["Concepto de cuenta"].unique()

    costos_operacion = float(obtener_o_cero(datos,"Costos Operación")["Total"][0])
    gastos_admon = float(obtener_o_cero(datos,"Gastos Admon")["Total"][0])
    ingreso_no_operacional = float(obtener_o_cero(datos,"Ingresos No Operacional")["Total"][0])
    costo_ventas = float(obtener_o_cero(datos,"Costos de venta")["Total"][0])
    ingreso_operacional = float(obtener_o_cero(datos,"Ingresos Operacional")["Total"][0])
    costos_servicios = float(obtener_o_cero(datos,"Costos Servicios")["Total"][0])
    utilidad = float(obtener_o_cero(datos,"Utilidad")["Total"][0])

    utilidad_bruta = float(ingreso_operacional) + float(costo_ventas)

    fig = go.Figure(go.Waterfall(
        name="Estado resultados",
        orientation = "v",
         measure = ["relative", "relative", "total", "relative","relative","relative","relative","total"],
          x = ["Ingreso operacional", "Costo ventas", "Utilidad bruta","ingreso no operacional","costo operacion","Gastos admmon","Costos Servicios","Utilidad"],
           textposition = "outside",
            text = [formatear_valor(ingreso_operacional),
                    formatear_valor(costo_ventas),
                    formatear_valor(utilidad_bruta),
                    formatear_valor(ingreso_no_operacional),
                    formatear_valor(costos_operacion),
                    formatear_valor(gastos_admon),
                    formatear_valor(costos_servicios),
                    formatear_valor(utilidad)
                    ],

            y = [ingreso_operacional, costo_ventas, utilidad_bruta,ingreso_no_operacional,costos_operacion,gastos_admon,costos_servicios,utilidad],

            connector = {"line":{"color":"rgb(63, 63, 63)"}}

    ))

    fig.update_layout(
        title = "Estado de resultados",
        title_x=0.5,
        xaxis_title="Periodo",
        yaxis_title="Partida",
        plot_bgcolor="white",   # fondo del área de trazado
        paper_bgcolor="white" 
)
    return fig