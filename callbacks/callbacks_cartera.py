from dash import Input, Output, callback,State,html,dcc
import dash_mantine_components as dmc
import pandas as pd
from dash.exceptions import PreventUpdate


from datos.preparacion_cartera import preparacion_datos_cartera
from utils.funciones_ayuda import formatear_valor
from utils.funciones_ayuda import parse_contents, cargar_notas_desde_store,guardar_notas_en_store
from graficos.cartera import grafico_deuda_cliente,grafico_deuda_cliente_estado,porcentaje_deuda_cliente,deuda_cliente_por_duracion_deuda,tabla_detalles

@callback(
    Output('output-data-upload', 'children'),
    Output("seleccion-centro-costos-cartera", "options"),
    Output("seleccion-cliente", "options"),
    Output("seleccion-estado-deuda", "options"),
    Output("total-cartera", "children"),
    Output("deuda-vencida", "children"),
    Output("deuda-por-vencer", "children"),
    Output("deuda-critica", "children"),
    Output("notas-cliente", "children"), 
    Output("grafico-deuda-cliente", "figure"),
    Output("grafico-deuda-cliente-estado", "figure"),
    Output("porcentaje-deuda-por-cliente", "figure"),
    Output("cliente-deuda-duracion", "figure"),
    Output("tabla-detalles", "children"),
    Output('store-notas-clientes', 'data'),
    Input('upload-data', 'contents'),
    Input("seleccion-centro-costos-cartera", "value"),
    Input("seleccion-cliente", "value"),
    Input("seleccion-estado-deuda", "value"),
    State('upload-data', 'filename'),
    State('store-notas-clientes', 'data'),
)
def actualizar_cartera(datos_cargados, centro_costos, cliente, estado_deuda, nombre_archivo, store_notas):
    if datos_cargados is None:
        return (
            [], [], [], [],
            "0", "0", "0", "0",
            [],
            {}, {}, {}, {},
            [],
            None  # ← Faltaba el output para store-notas-clientes
        )
    else:
        datos = parse_contents(datos_cargados, nombre_archivo)
        detalles_clientes = []
        datos_cartera = datos.copy()

        # ============ CREAR/ACTUALIZAR STORE CON TODOS LOS CLIENTES ============
        
        df_todos_clientes = datos.pivot_table(
            index=["Centro de costo", "Cliente"],
            columns="estado",
            values="Total cartera",
            aggfunc="sum",
            fill_value=0
        ).reset_index()
        
        # Asegurarse de que existan las columnas de estados
        for estado in ['Vencido', 'Por vencer']:
            if estado not in df_todos_clientes.columns:
                df_todos_clientes[estado] = 0
        
        # Añadir columna de Notas vacía si no existe
        if 'Notas' not in df_todos_clientes.columns:
            df_todos_clientes['Notas'] = ""
        
        # Si ya hay un store con notas, preservarlas
        if store_notas:
            df_store_existente = pd.DataFrame(store_notas)
            
            # Actualizar las notas existentes en el nuevo DataFrame
            for idx, row in df_store_existente.iterrows():
                mask = (
                    (df_todos_clientes['Centro de costo'] == row['Centro de costo']) & 
                    (df_todos_clientes['Cliente'] == row['Cliente'])
                )
                if mask.any() and row['Notas']:
                    df_todos_clientes.loc[mask, 'Notas'] = row['Notas']
        
        # Convertir a formato para el store
        store_data = df_todos_clientes.to_dict('records')

        centros_costos = datos_cartera['Centro de costo'].unique()

        # Actualizamos filtros
        if centro_costos:
            datos_cartera = datos_cartera[datos_cartera['Centro de costo'] == centro_costos]
        if cliente:
            datos_cartera = datos_cartera[datos_cartera['Cliente'] == cliente]
            detalles_clientes = tabla_detalles(datos_cartera)
        if estado_deuda:
            datos_cartera = datos_cartera[datos_cartera["estado"].isin(estado_deuda)]
        
        notas_cliente = []
        if cliente and centro_costos:
            # Buscar nota existente en df_todos_clientes (ya tiene las notas cargadas)
            nota_existente = ""
            mask = (
                (df_todos_clientes['Centro de costo'] == centro_costos) & 
                (df_todos_clientes['Cliente'] == cliente)
            )
            if mask.any():
                nota_existente = df_todos_clientes.loc[mask, 'Notas'].values[0]

            notas_cliente = dmc.Stack(
                children=[
                    dcc.Textarea(
                        id="notas",
                        placeholder="Escribe aquí las observaciones",
                        value=nota_existente,
                        style={'width': '100%', 'minHeight': '100px'}
                    ),
                    dmc.Button(
                        "Guardar Nota",
                        id="btn-guardar-nota",
                        color="blue",
                        mt=10
                    )
                ]
            )

        clientes = datos_cartera['Cliente'].unique()
        duraciones_deuda = datos["estado"].unique()

        # Actualizamos datos del total de la cartera
        total_cartera = datos_cartera["Total cartera"].sum()
        total_cartera = formatear_valor(total_cartera)
        
        # Actualizamos datos de la cartera vencida
        datos_cartera_vencida = datos_cartera[datos_cartera["estado"] == "Vencido"]
        cartera_vencida = datos_cartera_vencida["Total cartera"].sum()
        cartera_vencida = formatear_valor(cartera_vencida)

        # Actualizamos datos de la cartera por vencer
        datos_cartera_por_vencer = datos_cartera[datos_cartera["estado"] == "Por vencer"]
        cartera_al_dia = datos_cartera_por_vencer["Total cartera"].sum()
        cartera_al_dia = formatear_valor(cartera_al_dia)

        # Actualizamos datos de la cartera critica
        datos_deuda_critica = datos_cartera[datos_cartera["vencimiento"] <= -180]
        deuda_critica = datos_deuda_critica["Total cartera"].sum()
        deuda_critica = formatear_valor(deuda_critica)

        # Actualizamos gráficos
        barras_deuda_cliente = grafico_deuda_cliente(datos_cartera)
        barras_deuda_cliente_estado = grafico_deuda_cliente_estado(datos_cartera)
        grafico_porcentaje_deuda_cliente = porcentaje_deuda_cliente(datos_cartera)
        Grafico_deuda_cliente_por_duracion = deuda_cliente_por_duracion_deuda(datos_cartera)

        return (
            nombre_archivo, 
            centros_costos, 
            clientes, 
            duraciones_deuda, 
            total_cartera, 
            cartera_vencida, 
            cartera_al_dia, 
            deuda_critica,
            notas_cliente, 
            barras_deuda_cliente, 
            barras_deuda_cliente_estado,
            grafico_porcentaje_deuda_cliente, 
            Grafico_deuda_cliente_por_duracion, 
            detalles_clientes, 
            store_data  # ✅ Corregido: era df_todos_clientes
        )

    
@callback(
    Output('store-notas-clientes', 'data', allow_duplicate=True),  # ✅ Añadido allow_duplicate
    Output('notas', 'value'),
    Input('btn-guardar-nota', 'n_clicks'),
    State('notas', 'value'),
    State('seleccion-centro-costos-cartera', 'value'),
    State('seleccion-cliente', 'value'),
    State('store-notas-clientes', 'data'),
    prevent_initial_call=True
)
def guardar_nota(n_clicks, texto_nota, centro_costos, cliente, store_notas):
    if not n_clicks or not cliente or not centro_costos or not store_notas:
        raise PreventUpdate
    
    # Cargar DataFrame desde el store
    df_notas = pd.DataFrame(store_notas)
    
    # Actualizar la nota del cliente específico
    mask = (
        (df_notas['Centro de costo'] == centro_costos) & 
        (df_notas['Cliente'] == cliente)
    )
    
    if mask.any():
        df_notas.loc[mask, 'Notas'] = texto_nota or ""
    else:
        raise PreventUpdate
    
    # Convertir a formato store
    store_data = df_notas.to_dict('records')
    
    return store_data, texto_nota


@callback(
    Output("download-notas", "data"),
    Input("btn-descargar-notas", "n_clicks"),
    State('store-notas-clientes', 'data'),
    prevent_initial_call=True
)
def descargar_notas(n_clicks, store_notas):
    if not n_clicks or not store_notas:
        raise PreventUpdate
    
    df_notas = pd.DataFrame(store_notas)
    
    if df_notas.empty:
        raise PreventUpdate
    
    return dcc.send_data_frame(df_notas.to_excel, "notas_clientes.xlsx", index=False, sheet_name="Notas")