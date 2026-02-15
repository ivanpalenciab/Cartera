from datetime import datetime

import pandas as pd
import numpy as np


#inicialmente probaremos asi pero deberan obtenerse mediante frontend

def preparacion_datos_cartera(ruta):

    hoy = datetime.strptime(datetime.today().strftime("%d/%m/%Y"), "%d/%m/%Y")
    datos = pd.read_excel(ruta,header=6)
    datos['Fecha vencimiento'] = pd.to_datetime(datos['Fecha vencimiento'],format='%d/%m/%Y')
    datos["vencimiento"] = (datos['Fecha vencimiento'] - hoy)
    datos["estado"] = np.where(datos["vencimiento"].dt.days < 0, "Vencido", "Por vencer")
    datos["vencimiento"] = datos["vencimiento"].dt.days
    datos = datos[datos["Total cartera"] >= 0] # sacamos de la cuenta los que tienen saldos a favor
    
    datos["duracion_deuda"] = pd.cut(
        datos["vencimiento"],
        bins=[-float('inf'),-180,-90,-1,float('inf')],
        labels=[
            "mayor a 6 meses","entre 3 y 6 meses"," menor a 3 meses","al dia"
        ]
    )

    return datos