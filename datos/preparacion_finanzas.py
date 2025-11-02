import polars as pl
from babel.dates import format_date

def preparacion_datos_financieros(diccionario_datos):
    """Recibe un diccionario con los diferentes dataframes que se contienen en el archivo excel"""

    #obtenemos cada una de las tablas
    movimientos_cuentas_contables = diccionario_datos["Movimientos cuentas contables"]
    terceros = diccionario_datos['Terceros']
    cuentas =diccionario_datos['Cuentas']
    unidad_negocio=diccionario_datos['unidad negocio']
    material = diccionario_datos['Material']
    orden = diccionario_datos["Orden"]

    movimientos_cuentas_contables = movimientos_cuentas_contables.with_columns([
    pl.col("Cantidad").cast(pl.Float64), 
    pl.col("Fecha elaboración").dt.month().alias("mes_numero"),
     pl.col("Fecha elaboración").map_elements(
        lambda d: format_date(d, "MMMM", locale="es_CO"),
        return_dtype=pl.Utf8
    ).alias("mes")
    ])

    #unimos los datos de cada una de las tablas 

    datos_finanzas = movimientos_cuentas_contables.join(
                  terceros.select(['Identificación','Nombre tercero']),
                  left_on="Identificación tercero",
                  right_on = "Identificación",
                  how="left"
                  ).join(
                        cuentas.select(["Código cuenta contable","Clasificación1","Clasificación2",'Clasificación3 ']),
                        left_on = "Código cuentas contables",
                        right_on = "Código cuenta contable",
                        how="left"
                        ).join(
                            unidad_negocio,
                            left_on="Centro de Costos",
                            right_on = "Centro de Costos",
                            how="left"
                            ).join(
                                material,
                                left_on="Nombre producto",
                                right_on="Material",
                                how="left"
                                ).join(
                                        orden,
                                        left_on="Clasificación3 ",
                                        right_on="Tipo")
    datos_finanzas =datos_finanzas.rename({"Clasificación2":"Tipo de cuenta","Clasificación3 ":"Concepto de cuenta"})
    return datos_finanzas