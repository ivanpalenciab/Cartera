from dash import Input, Output, callback,State
import polars as pl


from datos.preparacion_cartera import preparacion_datos_cartera

@callback(
        Input("seleccion-centro-costos-cartera","value"),
        Input("seleccion-cliente","value")
)
def actualizar_cartera(centro_costos,cliente):
    pass