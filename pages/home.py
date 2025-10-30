import dash
import dash_mantine_components as dmc
from dash import Input, Output, callback
from dash import dcc,dash_table, Input, Output, State,html
import polars as pl
import numpy as np
import locale
import base64
import io

from datos.preparacion_finanzas import preparacion_datos_financieros

datos_crudos = pl.read_excel("datos/Base_datos_finanzas.xlsx",sheet_id=0)
datos = preparacion_datos_financieros(datos_crudos)
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
                    dcc.Dropdown(centros_costos,"",id="seleccion-semanas"),
                    html.Div(id="resultado-prediccion")
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ), 

                    dmc.GridCol(
                    children=[
                    dmc.Text("Elija unidad de negocio", size="sm", fw=500),
                    dcc.Dropdown(unidad_negocio,"",id="seleccion-semanas"),
                    html.Div(id="resultado-prediccion")
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ), 
                    
                        ])
                ]) )

                
                 

