from dash import Input, Output, callback,State
import polars as pl

from datos.preparacion_finanzas import preparacion_datos_financieros
from utils.funciones_ayuda import formatear_valor
from utils.funciones_ayuda import obtencion_estado_resultados
from graficos.estado_resultados import grafico_linea_estado_resultados, grafico_cascada
from graficos.unidades_negocio import grafico_barras_ingresos_por_unidad_negocio,tabla_unidad_negocio

@callback(
    Output("estado-resultados", "data"),
    Output("seleccion-centro-costos","options"),
    Output("seleccion-unidad-negocio","options"),
    Output("grafico-estado-resultados","figure"),
    Output("grafico-cascada-estado-resultados","figure"),
    Output("grafico-ingresos-unidad-negocio","figure"),
    Output("tabla-ingresos-unidad-negocio","data"),
    Input("seleccion-unidad-negocio","value"),
    Input("seleccion-centro-costos","value")
)
def actualizar_datos(unidad_negocio,centro_costos):

    #voy accceder a los datos de forma local dentro de la función
    datos_crudos = pl.read_excel("datos/Base_datos_finanzas.xlsx",sheet_id=0)
    datos = preparacion_datos_financieros(datos_crudos)

    datos = datos.clone()

    if unidad_negocio:
        datos = datos.filter(pl.col("Unidad de negocio")==unidad_negocio)
    if centro_costos:
        datos = datos.filter(pl.col("Centro de Costos")==centro_costos)

    centros_costos = datos["Centro de Costos"].unique().to_list()

    unidades_negocio = datos["Unidad de negocio"].unique().to_list()

    datos_estado_resultado, ingreso_operacional,costo_ventas,utilidad = obtencion_estado_resultados(datos)

    figura = grafico_linea_estado_resultados(ingreso_operacional,costo_ventas,utilidad)

    cascada = grafico_cascada(datos_estado_resultado)


    #formateamos el valor
    datos_estado_resultado = datos_estado_resultado.with_columns([
        pl.col(c).map_elements(formatear_valor).alias(c)
    for c in datos_estado_resultado.columns if c != "Concepto de cuenta"])

    #aqui iniciamos a mostrar los datos correspondientes a los graficos de unidades de negocio

    ingresos_unidad_negocio = grafico_barras_ingresos_por_unidad_negocio(datos)

    datos_tabla_unidad_negocio = tabla_unidad_negocio(datos)

    return datos_estado_resultado.to_dicts(),centros_costos,unidades_negocio,figura,cascada,ingresos_unidad_negocio,datos_tabla_unidad_negocio.to_dicts()