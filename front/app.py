import dash
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, State
from dash_iconify import DashIconify
import requests
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN
app = dash.Dash(__name__)
server = app.server
API_URL = os.getenv("API_URL", "http://localhost:8000")

# --- CARGA DE DATOS HISTÓRICOS ---
try:
    df = pd.read_csv('datos_historicos.csv')
    
    # KPIs
    total_viajeros = len(df)
    gasto_promedio = df['gasto_total_pesos'].mean()
    estancia_promedio = df['duracion_estadia'].mean()
    gasto_total_anio = df['gasto_total_pesos'].sum() # Suma total de la muestra
    
    # Gráfica 1: Motivos
    top_motivos = df['motivo'].value_counts().head(5)
    fig_motivos = px.bar(x=top_motivos.values, y=top_motivos.index, orientation='h', 
                         title="Top 5 Motivos de Viaje", template="plotly_white",
                         labels={'x': 'Viajeros', 'y': ''})
    fig_motivos.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=300)
    fig_motivos.update_traces(marker_color='#339af0')

    # Gráfica 2: Alojamiento (NUEVA)
    top_alojamiento = df['alojamiento'].value_counts().head(5)
    fig_alojamiento = px.bar(x=top_alojamiento.values, y=top_alojamiento.index, orientation='h',
                             title="Preferencias de Alojamiento", template="plotly_white",
                             labels={'x': 'Viajeros', 'y': ''})
    fig_alojamiento.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=300)
    fig_alojamiento.update_traces(marker_color='#40c057')

except Exception as e:
    print(f"⚠️ Error cargando históricos: {e}")
    total_viajeros = 0
    gasto_promedio = 0
    estancia_promedio = 0
    gasto_total_anio = 0
    fig_motivos = {}
    fig_alojamiento = {}

# Helper para Tarjetas KPI
def crear_kpi(titulo, valor, icono, color):
    return dmc.Paper(
        shadow="md", radius="md", p="md", withBorder=True,
        children=[
            dmc.Group(position="apart", children=[
                dmc.Text(titulo, color="dimmed", size="xs", weight=700, transform="uppercase"),
                dmc.ThemeIcon(DashIconify(icon=icono, width=20), color=color, variant="light", size="lg")
            ]),
            dmc.Text(valor, size="xl", weight=700, style={"marginTop": 10})
        ]
    )

def get_icon(icon):
    return DashIconify(icon=icon, height=20)

# ---------------------------------------------------------
# 2. LAYOUT VISUAL
# ---------------------------------------------------------
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    theme={"colorScheme": "light"},
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Container(size="xl", style={"marginTop": 30, "marginBottom": 50}, children=[
            
            # Encabezado
            dmc.Group(spacing="xs", children=[
                DashIconify(icon="emojione:airplane", height=35),
                dmc.Title("Inteligencia Turística Bogotá", order=2, color="blue"),
            ]),
            dmc.Text("Análisis descriptivo 2023 y Proyecciones IA", color="dimmed"),
            dmc.Divider(my="md"),

            # --- SECCIÓN 1: KPIs (4 Tarjetas) ---
            dmc.SimpleGrid(cols=4, spacing="lg", breakpoints=[{"maxWidth": "sm", "cols": 1}], children=[
                crear_kpi("Viajeros Analizados", f"{total_viajeros:,.0f}", "mdi:account-group", "blue"),
                crear_kpi("Gasto Promedio / Pers", f"${gasto_promedio:,.0f}", "mdi:cash-multiple", "green"),
                crear_kpi("Estancia Promedio", f"{estancia_promedio:.1f} Días", "mdi:calendar-clock", "orange"),
                crear_kpi("Impacto Económico", f"${gasto_total_anio:,.0f}", "mdi:bank", "grape"),
            ]),
            
            dmc.Space(h=30),

            # --- SECCIÓN 2: GRÁFICAS ---
            dmc.Grid(children=[
                dmc.Col(span=12, md=6, children=[
                    dmc.Paper(shadow="sm", p="md", withBorder=True, children=[dcc.Graph(figure=fig_motivos)])
                ]),
                dmc.Col(span=12, md=6, children=[
                    dmc.Paper(shadow="sm", p="md", withBorder=True, children=[dcc.Graph(figure=fig_alojamiento)])
                ]),
            ]),

            dmc.Space(h=50),
            dmc.Divider(label="PREDICTOR EN TIEMPO REAL", labelPosition="center", size="sm"),
            dmc.Space(h=20),

            # --- SECCIÓN 3: CALCULADORA IA ---
            dmc.Paper(shadow="xl", radius="lg", p="xl", withBorder=True, style={"borderColor": "#228be6"}, children=[
                dmc.Text("Simulador de Gasto Futuro", size="lg", weight=600, mb="lg", align="center"),
                
                dmc.Grid(children=[
                    dmc.Col(span=12, md=4, children=[
                        dmc.NumberInput(
                            id="input-duracion", label="Duración (Noches)", value=3, min=1,
                            icon=get_icon("radix-icons:calendar"), style={"width": "100%"}
                        )
                    ]),
                    dmc.Col(span=12, md=4, children=[
                        dmc.Select(
                            id="input-motivo", label="Motivo", value='a. Vacaciones/recreación/Ocio',
                            icon=get_icon("radix-icons:person"),
                            data=[
                                {'label': '🏖️ Vacaciones', 'value': 'a. Vacaciones/recreación/Ocio'},
                                {'label': '💼 Negocios', 'value': 'g. Negocios y motivos profesionales'},
                                {'label': '🏠 Familia', 'value': 'b. Visita a familiares y amigos'},
                                {'label': '🎓 Educación', 'value': 'c. Educación y formación'},
                                {'label': '🏥 Salud', 'value': 'd. Salud , Bienestar y atención médica'},
                                {'label': '🛍️ Compras', 'value': 'f. Compras'},
                                {'label': 'i. Otro', 'value': 'i. Otro.'}
                            ], style={"width": "100%"}
                        )
                    ]),
                    dmc.Col(span=12, md=4, children=[
                        dmc.Select(
                            id="input-alojamiento", label="Alojamiento", value='a. Hotel',
                            icon=get_icon("radix-icons:home"),
                            data=[
                                {'label': '🏨 Hotel', 'value': 'a. Hotel'},
                                {'label': '🎒 Hostal', 'value': 'b. Hostal'},
                                {'label': '🏢 Apartahotel', 'value': 'c. Apartahotel'},
                                {'label': '📱 Airbnb', 'value': 'd. Inmueble de alquiler (pagos por plataforma dig)'},
                                {'label': '🏠 Casa Amigos', 'value': 'e. Casa propia, de familiares o amigos (sin pago)'},
                                {'label': 'f. Otro', 'value': 'f. Otro'}
                            ], style={"width": "100%"}
                        )
                    ]),
                ]),
                
                dmc.Space(h=30),
                dmc.Button(
                    "Calcular Predicción con IA", id="btn-predecir", 
                    variant="gradient", gradient={"from": "indigo", "to": "cyan"}, 
                    fullWidth=True, size="lg"
                ),
                
                dmc.Space(h=20),
                dmc.LoadingOverlay(html.Div(id="resultado-container"))
            ]),

            # Switch Dark Mode
            dmc.Space(h=30),
            dmc.Group(position="right", children=[
                dmc.Switch(id="theme-switch", size="lg", onLabel=DashIconify(icon="radix-icons:moon"), offLabel=DashIconify(icon="radix-icons:sun"))
            ])
        ])
    ]
)

# ---------------------------------------------------------
# 3. CALLBACKS
# ---------------------------------------------------------
@app.callback(Output("mantine-provider", "theme"), Input("theme-switch", "checked"))
def update_theme(checked):
    return {"colorScheme": "dark" if checked else "light"}

@app.callback(
    Output('resultado-container', 'children'),
    Input('btn-predecir', 'n_clicks'),
    State('input-duracion', 'value'),
    State('input-motivo', 'value'),
    State('input-alojamiento', 'value'),
    prevent_initial_call=True
)
def realizar_prediccion(n_clicks, duracion, motivo, alojamiento):
    payload = {"duracion": int(duracion), "motivo": motivo, "alojamiento": alojamiento}
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        if response.status_code == 200:
            valor = response.json()["gasto_estimado"]
            return dmc.Alert(
                title="Estimación Exitosa", color="green", variant="filled",
                children=[
                    dmc.Group(position="apart", children=[
                        dmc.Text("Cálculo procesado vía API Remota:"),
                        dmc.Badge("Estimación Exitosa", color="lime")
                    ]),
                    dmc.Space(h=10),
                    dmc.Text(f"${valor:,.0f} COP", size="xl", weight=700)
                ],
                icon=DashIconify(icon="mdi:check-circle", height=30)
            )
        else:
            return dmc.Alert(title="Error API", color="red", children=f"La API respondió: {response.text}")
    except Exception as e:
        return dmc.Alert(title="Error Conexión", color="red", children=f"No se pudo conectar a {API_URL}. Detalle: {e}")

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
