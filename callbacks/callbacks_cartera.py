from dash import Input, Output, callback,State
import polars as pl


from datos.preparacion_cartera import preparacion_datos_cartera
from utils.funciones_ayuda import formatear_valor

@callback(
       
        Output("seleccion-centro-costos-cartera","options"),
        Output("seleccion-cliente","options"),
        Output("total-cartera","children"),
        Output("deuda-vencida","children"),
        Output("deuda-por-vencer","children"),
        Output("deuda-critica","children"),
        Input("seleccion-centro-costos-cartera","value"),
        Input("seleccion-cliente","value")
)
def actualizar_cartera(centro_costos,cliente):
    
    #los datoos aqui estan siendo procesados en pandas pero deben pasara 
    #a ser procesados con polars
    datos_cartera = preparacion_datos_cartera()

    #datos_cartera = datos_cartera.clone()

    if centro_costos:
        datos_cartera = datos_cartera[datos_cartera['Centro de costo']==centro_costos]
    if cliente:
        datos_cartera = datos_cartera[datos_cartera['Cliente']==cliente]

    centros_costos = datos_cartera['Centro de costo'].unique()
    clientes = datos_cartera['Cliente'].unique()

    total_cartera = datos_cartera["Total cartera"].sum()
    total_cartera = formatear_valor(total_cartera)

    datos_cartera_vencida = datos_cartera[datos_cartera["estado"]=="Vencido"]
    cartera_vencida = datos_cartera_vencida["Total cartera"].sum()
    cartera_vencida = formatear_valor(cartera_vencida)

    datos_cartera_por_vencer = datos_cartera[datos_cartera["estado"]=="Por vencer"]
    cartera_al_dia = datos_cartera_por_vencer["Total cartera"].sum()
    cartera_al_dia = formatear_valor(cartera_al_dia)

    datos_deuda_critica = datos_cartera[datos_cartera["vencimiento"]<=-90]
    deuda_critica = datos_deuda_critica["Total cartera"].sum()
    deuda_critica = formatear_valor(deuda_critica)

    return centros_costos,clientes,total_cartera,cartera_vencida,cartera_al_dia,deuda_critica