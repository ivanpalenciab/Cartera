import numpy as np
import polars as pl

#polar_data = pl.read_excel("Datos/Base_datos_finanzas.xlsx",sheet_id=0)

def preparacion_datos_financieros(diccionario_datos):
    """Recibe un diccionario con los diferentes dataframes que se contienen en el archivo excel"""

    #obtenemos cada una de las tablas
    movimientos_cuentas_contables = diccionario_datos["Movimientos cuentas contables"]
    terceros = diccionario_datos['Terceros']
    cuentas =diccionario_datos['Cuentas']
    unidad_negocio=diccionario_datos['unidad negocio']
    material = diccionario_datos['Material']

    movimientos_cuentas_contables = movimientos_cuentas_contables.with_columns([
    pl.col("Cantidad").cast(pl.Float64), 
    pl.col("Fecha elaboración").dt.strftime("%B").alias("mes")
    ])

    #unimos los datos de cada una de las tablas 
    datos_finanzas = movimientos_cuentas_contables.join(
                  terceros.select(['Identificación','Nombre tercero']),
                  left_on="Identificación tercero",
                  right_on = "Identificación"
                  ).join(
                        cuentas.select(["Código cuenta contable","Clasificación1","Clasificación2",'Clasificación3 ']),
                        left_on = "Código cuentas contables",
                        right_on = "Código cuenta contable"
                        ).join(
                            unidad_negocio,
                            left_on="Centro de Costos",
                            right_on = "Centro de Costos"
                            ).join(
                                material,
                                left_on="Nombre producto",
                                right_on="Material"
                            )
    return datos_finanzas
