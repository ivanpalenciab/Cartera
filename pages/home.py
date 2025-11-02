import dash
import dash_mantine_components as dmc
from dash import Input, Output, callback
from dash import dcc,dash_table, Input, Output, State,html
import polars as pl
import numpy as np
import locale
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

from datos.preparacion_finanzas import preparacion_datos_financieros
from graficos.estado_resultados import grafico_estado_resultados
from utils.funciones_ayuda import obtencion_estado_resultados

datos_crudos = pl.read_excel("datos/Base_datos_finanzas.xlsx",sheet_id=0)
datos = preparacion_datos_financieros(datos_crudos)
datos_estado_resultados = obtencion_estado_resultados(datos)

centros_costos = datos["Centro de Costos"].unique().to_list()
unidad_negocio = datos["Unidad de negocio"].unique().to_list()


dash.register_page(__name__, path="/", name="Inicio")

layout = dmc.MantineProvider(
    dmc.Container([

                  dmc.Group([
                    dmc.Text(
                        "Dashboard de informacion financiera",
                        size="xl",
                        fw=700,
                        ta="center",
                        c="#323C73",
                        style={"flexGrow": 1, "textAlign": "center"}
                    ),
                    html.Img(src="/assets/logo.png", style={"height": "50px"})
                ], justify="space-between", style={"marginBottom": "20px"}),

                dmc.Grid([
                    dmc.GridCol(
                    children=[
                    dmc.Text("Elija centro de costos", size="sm", fw=500),
                    dcc.Dropdown(
                        options= [],
                        id="seleccion-centro-costos"),
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ), 

                    dmc.GridCol(
                    children=[
                    dmc.Text("Elija unidad de negocio", size="sm", fw=500),
                    dcc.Dropdown(
                        options= datos["Unidad de negocio"].unique().to_list(),
                        id="seleccion-unidad-negocio"),
                    html.Div(id="resultado-prediccion")
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ), 
                    
                        ]),
                
                dmc.Grid([
                    dmc.GridCol(
                        children =[
                            grafico_estado_resultados(datos_estado_resultados)
                        ]
                    )
                ])    
                ]) )