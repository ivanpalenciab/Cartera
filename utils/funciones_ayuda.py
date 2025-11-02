import polars as pl

def formatear_valor(val):
    """Convierte 1420874.98 → 1.420.874,98"""
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def obtencion_estado_resultados(datos):
     datos_estado_resultado = datos.filter(pl.col("Clasificación1")=="Estado Resultados")
     datos_estado_resultado = datos_estado_resultado.select(["Concepto de cuenta","Neto","mes","mes_numero","Orden"])

     datos_estado_resultado = datos_estado_resultado.group_by(["Concepto de cuenta","mes","mes_numero","Orden"]
                                                              ).agg(pl.col("Neto").sum()
                                                              ).with_columns((pl.col("Neto") * -1).alias("Neto")
                                                                ).sort(["mes_numero","Orden"])
     
     datos_estado_resultado = datos_estado_resultado.pivot("mes",index="Concepto de cuenta", values="Neto")
     datos_estado_resultado = datos_estado_resultado.with_columns(
    pl.sum_horizontal(
        [col for col in datos_estado_resultado.columns if col != "Concepto de cuenta"]
    ).alias("Total"))

    #obtenemos el total
     fila_total = pl.DataFrame({
    "Concepto de cuenta": ["Utilidad"],
    **{col: [datos_estado_resultado[col].sum()] for col in datos_estado_resultado.columns 
       if col != "Concepto de cuenta" }})
     
     datos_estado_resultado = pl.concat([datos_estado_resultado, fila_total])

    #formateamos el valor
     datos_estado_resultado = datos_estado_resultado.with_columns([
        pl.col(c).map_elements(formatear_valor).alias(c)
    for c in datos_estado_resultado.columns if c != "Concepto de cuenta"])
     
     return datos_estado_resultado 