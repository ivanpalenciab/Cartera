import dash
import dash_mantine_components as dmc
from dash import dcc,dash_table,html
import locale
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div([
    dcc.Location(id="redirect-home", pathname="/dashboard-cartera")
])