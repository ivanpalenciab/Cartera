import dash
import dash_mantine_components as dmc
from dash import dcc,dash_table,html
import polars as pl
import locale
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

from datos.preparacion_finanzas import preparacion_datos_financieros
from graficos.estado_resultados import grafico_estado_resultados
from utils.funciones_ayuda import obtencion_estado_resultados
from utils.header import header
import callbacks.callbacks

datos_crudos = pl.read_excel("datos/Base_datos_finanzas.xlsx",sheet_id=0)
datos = preparacion_datos_financieros(datos_crudos)
datos_estado_resultados,ingreso_operacional,costo_ventas, utilidad = obtencion_estado_resultados(datos)

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
                header(),

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
                        id="seleccion-unidad-negocio")
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
                ]),
                dmc.Grid([
                     dmc.GridCol(
                        dcc.Graph(id="grafico-estado-resultados", figure={}),
                        span=6  # Ocupa la mitad de la fila
                        ),
                        dmc.GridCol(
                            dcc.Graph(id="grafico-cascada-estado-resultados", figure={}),
                            span=6  # Ocupa la otra mitad
                    )
                ],  gutter="xs"),
                dmc.Grid([
                     
                        dmc.GridCol(
                            dash_table.DataTable(
                                id="tabla-ingresos-unidad-negocio",
                                data=[], 
                                style_table={'overflowX': 'auto'},
                                style_cell={
                                    "textAlign": "center",
                                    "fontSize": "9px",
                                    "padding": "1px 2px",
                                    "whiteSpace": "nowrap",  # no permite saltos, pero ocupa menos espaci
                                },),
                           
                            span=6  # Ocupa la otra mitad
                    ),dmc.GridCol(
                        dcc.Graph(id="grafico-ingresos-unidad-negocio", figure={}),
                        span=6  # Ocupa la mitad de la fila
                        ),
                ],  gutter="xs")     
                ],
            fluid=True, 
            style={"paddingLeft": "2%", "paddingRight": "2%"}) )