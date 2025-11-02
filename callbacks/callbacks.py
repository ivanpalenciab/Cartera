from dash import Input, Output, callback,State
import polars as pl

from datos.preparacion_finanzas import preparacion_datos_financieros
from utils.funciones_ayuda import formatear_valor
from utils.funciones_ayuda import obtencion_estado_resultados

@callback(
    Output("estado-resultados", "data"),
    Output("seleccion-centro-costos","options"),
    Output("seleccion-unidad-negocio","options"),
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

    #datos_estado_resultado = datos.filter(pl.col("Clasificación1")=="Estado Resultados")

    #datos_estado_resultado = datos_estado_resultado.select(["Concepto de cuenta","Neto","mes"])

    #datos_estado_resultado = datos_estado_resultado.group_by(["Concepto de cuenta","mes"]).agg(pl.col("Neto").sum())

    #datos_estado_resultado = datos_estado_resultado.pivot("mes",index="Concepto de cuenta", values="Neto")

    #formateamos los valores
    #datos_estado_resultado = datos_estado_resultado.with_columns([
    #pl.col(c).map_elements(formatear_valor).alias(c)
    #for c in datos_estado_resultado.columns if c != "Concepto de cuenta"])

    datos_estado_resultado = obtencion_estado_resultados(datos)

    return datos_estado_resultado.to_dicts(),centros_costos,unidades_negocio