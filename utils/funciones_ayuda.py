import polars as pl

def formatear_valor(val):
    """Convierte 1420874.98 → 1.420.874,98"""
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def obtener_o_cero(df, concepto):
    filtrado = df.filter(pl.col("Concepto de cuenta") == concepto)
    if filtrado.is_empty():
        # Crear un DataFrame con las mismas columnas y valores en cero
        columnas = df.columns
        # Creamos una fila con ceros del mismo tipo que las columnas numéricas
        cero_dict = {col: [0] if df[col].dtype in [pl.Int64, pl.Float64] else [concepto] for col in columnas}
        filtrado = pl.DataFrame(cero_dict)
    return filtrado

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

     #definimos la dats para grafico de lineas
     ingresos_operacionales = obtener_o_cero(datos_estado_resultado,"Ingresos Operacional")
     
     costos_ventas = obtener_o_cero(datos_estado_resultado,"Costos de venta")
     costos_ventas = costos_ventas.fill_null(0)

     utilidad = obtener_o_cero(datos_estado_resultado,"Utilidad")
     
     return datos_estado_resultado, ingresos_operacionales,costos_ventas,utilidad 