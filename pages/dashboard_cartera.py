import dash
from dash import dcc,dash_table, Input, Output, State,html
import dash_mantine_components as dmc

from utils.header import header
from graficos.tarjeta import tarjeta_kpi
import callbacks.callbacks_cartera

dash.register_page(__name__, path="/dashboard-cartera", name="Dasboard Cartera")


layout = dmc.MantineProvider(
    dmc.Container([
         dmc.Group([
                    dmc.Text(
                        "Dashboard de cartera",
                        size="xl",
                        fw=700,
                        ta="center",
                        c="#323C73",
                        style={"flexGrow": 1, "textAlign": "center"}
                    ),
                    html.Img(src="/assets/logo.png", style={"height": "50px"})
                ], justify="space-between", style={"marginBottom": "20px"}),
        header(),
        dmc.Grid([
                dmc.GridCol(
                    children=[
                    dcc.Upload(id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ), 
                       ]),
            dmc.Grid([
                dmc.GridCol(
                    children=[
                    dmc.Text("Elija centro de costos", size="sm", fw=500),
                    dcc.Dropdown(
                        options= [],
                        id="seleccion-centro-costos-cartera"),
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ), 

                    dmc.GridCol(
                    children=[
                    dmc.Text("Elija Cliente", size="sm", fw=500),
                    dcc.Dropdown(
                        options= [],
                        id="seleccion-cliente")
                    ],span=4,
                    #style={"marginTop": "100px"}
                    ),
                       ]),
            dmc.Grid([
                dmc.GridCol(
                    children=[
                                tarjeta_kpi("Total deuda",0,"#323C73","total-cartera")
                    ],span=3),
                dmc.GridCol(
                    children = [
                        tarjeta_kpi("Deuda Vencida",0,"#323C73","deuda-vencida")
                    ],span=3),
                dmc.GridCol(
                    children=[
                        tarjeta_kpi("Deuda por vencer",0,"#323C73","deuda-por-vencer")
                    ],span=3),
                dmc.GridCol(
                    children=[
                        tarjeta_kpi("Deuda critica",0,"#323C73","deuda-critica") #deuda con mas de 90 dias vencidas
                    ], span=3)

            ]),
            dmc.Grid([
                dmc.GridCol(
                    children = [
                        dcc.Graph(id="grafico-deuda-cliente",figure={})
                    ],span=6),
                dmc.GridCol(
                    children = [
                        dcc.Graph(id="grafico-deuda-cliente-estado",figure={})
                    ],span=6
                )
            ]),
            dmc.Grid([
                dmc.GridCol(
                    children = [
                        dcc.Graph(id="porcentaje-deuda-por-cliente",figure={})
                    ],span=6),
                dmc.GridCol(
                    children = [
                        dcc.Graph(id="cliente-deuda-duracion",figure={})
                    ],span=6
                )
            ])
                         ],
                         fluid=True, 
                        style={"paddingLeft": "2%", "paddingRight": "2%"})
                        
                        )
