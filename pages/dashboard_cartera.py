import dash
from dash import dcc,dash_table, Input, Output, State,html

dash.register_page(__name__, path="/dashboard-cartera", name="Dasboard Cartera")

layout = html.Div(["aqui va el dashboard"])