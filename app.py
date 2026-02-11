import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import os 

#import callbacks.callbacks

app = Dash(__name__, suppress_callback_exceptions=True,use_pages=True)

app.layout = dmc.MantineProvider(dmc.Container([
 dash.page_container
],fluid=True))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)