from dash import dash_table
import polars as pl

from utils.funciones_ayuda import formatear_valor

def grafico_estado_resultados(datos):
   # datos_estado_resultado = datos.filter(pl.col("Clasificación1")=="Estado Resultados")

   # datos_estado_resultado = datos_estado_resultado.select(["Concepto de cuenta","Neto","mes"])

    #datos_estado_resultado = datos_estado_resultado.group_by(["Concepto de cuenta","mes"]).agg(pl.col("Neto").sum())

    #datos_estado_resultado = datos_estado_resultado.pivot("mes",index="Concepto de cuenta", values="Neto")

    #formateamos el valor 
    #datos_estado_resultado = datos_estado_resultado.with_columns([
    #pl.col(c).map_elements(formatear_valor).alias(c)
    #for c in datos_estado_resultado.columns if c != "Concepto de cuenta"
#])

    return dash_table.DataTable(
        id="estado-resultados",
        data=datos.to_dicts(), 
        style_table={'overflowX': 'auto'},
        style_cell={
            "textAlign": "center",
            "fontSize": "9px",
            "padding": "1px 2px",
            "whiteSpace": "nowrap",  # no permite saltos, pero ocupa menos espaci
        },
        )