import dash_mantine_components as dmc

def tarjeta_kpi(titulo, valor, color="blue",id=None):
    return dmc.Paper(
        shadow="sm",
        radius="md",
        p="md",
        withBorder=True,
        style={
            "textAlign": "center",
            "height": "120px",
            "width": "200px",             # Tamaño fijo opcional
            "backgroundColor":"w",     # Fondo personalizable
            "display": "flex",            # Centrado vertical
            "flexDirection": "column",
            "justifyContent": "center",
            "marginLeft": "30px", 
            "marginRight": "30px"
        },
        children=[
            dmc.Text(titulo, size="sm", fw=500, c="#323C73"),
            dmc.Text(f"{valor}",id=id, size="xl", fw=700, c=color, mt=10),
        ]
    )
