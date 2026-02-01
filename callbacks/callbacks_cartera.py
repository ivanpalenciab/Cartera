from dash import Input, Output, callback,State
import polars as pl


from datos.preparacion_cartera import preparacion_datos_cartera
from utils.funciones_ayuda import formatear_valor
from graficos.cartera import grafico_deuda_cliente,grafico_deuda_cliente_estado,porcentaje_deuda_cliente

@callback(
       
        Output("seleccion-centro-costos-cartera","options"),
        Output("seleccion-cliente","options"),
        Output("total-cartera","children"),
        Output("deuda-vencida","children"),
        Output("deuda-por-vencer","children"),
        Output("deuda-critica","children"), 
        Output("grafico-deuda-cliente","figure"),
        Output("grafico-deuda-cliente-estado","figure"),
        Output("porcentaje-deuda-por-cliente","figure"),
        Input("seleccion-centro-costos-cartera","value"),
        Input("seleccion-cliente","value")
)
def actualizar_cartera(centro_costos,cliente):
    
    #los datoos aqui estan siendo procesados en pandas pero deben pasara 
    #a ser procesados con polars
    datos_cartera = preparacion_datos_cartera()
    centros_costos = datos_cartera['Centro de costo'].unique()

    #datos_cartera = datos_cartera.clone()

    #actualizamos filtros
    if centro_costos:
        datos_cartera = datos_cartera[datos_cartera['Centro de costo']==centro_costos]
    if cliente:
        datos_cartera = datos_cartera[datos_cartera['Cliente']==cliente]


    clientes = datos_cartera['Cliente'].unique()

    #actualizamos datos del total de la cartera
    total_cartera = datos_cartera["Total cartera"].sum()
    total_cartera = formatear_valor(total_cartera)

    #actualizamos datos de la cartera vencida
    datos_cartera_vencida = datos_cartera[datos_cartera["estado"]=="Vencido"]
    cartera_vencida = datos_cartera_vencida["Total cartera"].sum()
    cartera_vencida = formatear_valor(cartera_vencida)


    #actualizamos datos de la cartera por vencer
    datos_cartera_por_vencer = datos_cartera[datos_cartera["estado"]=="Por vencer"]
    cartera_al_dia = datos_cartera_por_vencer["Total cartera"].sum()
    cartera_al_dia = formatear_valor(cartera_al_dia)

    #actualizamos datos de la cartera critica, deudas de mas de tres meses
    datos_deuda_critica = datos_cartera[datos_cartera["vencimiento"]<=-90]
    deuda_critica = datos_deuda_critica["Total cartera"].sum()
    deuda_critica = formatear_valor(deuda_critica)

    #actualizamos grafico de deuda por cliente 
    barras_deuda_cliente = grafico_deuda_cliente(datos_cartera)

    #actualizamos grafico de deuda por cliente y estado

    barras_deuda_cliente_estado = grafico_deuda_cliente_estado(datos_cartera)

    #actualizamos porcentaje de deuda por cliente
    grafico_porcentaje_deuda_cliente = porcentaje_deuda_cliente(datos_cartera)

    #actualizamos p

    return centros_costos,clientes,total_cartera,cartera_vencida,cartera_al_dia,deuda_critica,barras_deuda_cliente,barras_deuda_cliente_estado,grafico_porcentaje_deuda_cliente