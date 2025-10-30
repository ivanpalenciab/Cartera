import dash
import dash_mantine_components as dmc
from dash import Input, Output, callback
from dash import dcc,dash_table, Input, Output, State,html
import pandas as pd
import numpy as np
import locale
import base64
import io

from datos.preparacion import preparacion_datos

dash.register_page(__name__, path="/", name="Inicio")

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def formatear_valor(val):
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

layout = html.Div([
     #dcc.Store(id='shared-data', storage_type='memory'),
    #dash.page_container,
     html.H2("Cargar archivo Excel desde el frontend"),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra o haz clic para subir un archivo Excel'
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    
    html.Div(id='output-data')
])

 #=== CALLBACK ===
@callback(  
    Output('output-data', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return "Sube un archivo Excel para continuar."

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Leer Excel en DataFrame
        df = pd.read_excel(io.BytesIO(decoded))
        df = preparacion_datos(df)
    except Exception as e:
        return f"Error al leer el archivo: {e}"
    
    data_json = df.to_json(date_format='iso', orient='split')

    # Mostrar una vista previa de los datos
    return html.Div([
        html.H5(f"Archivo cargado: {filename}"),
        html.Hr(),
         dash_table.DataTable(
              id="datos",
                data=df.to_dict('records'), 
                page_size=12, 
                style_table={'overflowX': 'auto'}
         ),
        html.Div(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}"),
    ])


