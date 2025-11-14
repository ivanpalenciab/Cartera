import dash_mantine_components as dmc
from dash import html, dcc

def header():
    return html.Div([

        dmc.Grid([
            dmc.GridCol(
                dmc.Tabs(
                    [
                        
                        dmc.TabsList([
                            dmc.TabsTab(dcc.Link("Inicio", href="/"), value="/"),
                            dmc.TabsTab(dcc.Link("Cartera",href="/dashboard-cartera"),value="/dashboard-cartera"),
                            #dmc.TabsTab(dcc.Link("Flujo",href="/flujo"), value="/Flujo")
                           
                        ])
                    ],
                    value="/"  # <- esto resalta la pestaña actual
                ),
                span=6,
                style={"marginBottom": "20px"}
            )
        ])
    ])