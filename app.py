import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

import callbacks.callbacks

app = Dash(__name__, suppress_callback_exceptions=True,use_pages=True)

app.layout = dmc.MantineProvider(dmc.Container([
 dash.page_container
],fluid=True))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)