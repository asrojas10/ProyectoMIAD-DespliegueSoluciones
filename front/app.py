import dash
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, State
from dash_iconify import DashIconify
import requests
import os

# 1. CONFIGURACIÓN
app = dash.Dash(__name__)
server = app.server

# URL de la API (Variable de entorno)
# En local busca en localhost:8000, en la nube usará la variable que configures en Railway
API_URL = os.getenv("API_URL", "http://localhost:8000")
print(f"🚨 DEBUG: La URL que estoy viendo es: '{API_URL}'")

# Función auxiliar para íconos
def get_icon(icon):
    return DashIconify(icon=icon, height=20)

# ---------------------------------------------------------
# 2. LAYOUT (DISEÑO VISUAL)
# ---------------------------------------------------------
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    theme={"colorScheme": "light"},
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Container(size="sm", style={"marginTop": 40}, children=[
            
            # Encabezado
            dmc.Group(position="center", spacing="xs", children=[
                DashIconify(icon="emojione:airplane", height=40),
                dmc.Title("Predictor de Gasto Turístico", order=2, color="blue"),
            ]),
            dmc.Text("Inteligencia Artificial para el Turismo en Bogotá", color="dimmed", align="center", size="sm"),
            
            dmc.Space(h=30),

            # Tarjeta Principal
            dmc.Paper(shadow="xl", radius="lg", p="xl", withBorder=True, children=[
                
                # Grid de Inputs
                dmc.Grid(children=[
                    
                    # 1. Duración
                    dmc.Col(span=12, children=[
                        dmc.NumberInput(
                            id="input-duracion",
                            label="Duración del Viaje",
                            description="¿Cuántas noches se quedará?",
                            value=3,
                            min=1,
                            icon=get_icon("radix-icons:calendar"),
                            style={"width": "100%"}
                        ),
                    ]),

                    # 2. Motivo
                    dmc.Col(span=12, children=[
                        dmc.Select(
                            id="input-motivo",
                            label="Motivo Principal",
                            description="Seleccione la razón del viaje",
                            value='a. Vacaciones/recreación/Ocio',
                            icon=get_icon("radix-icons:person"),
                            data=[
                                {'label': '🏖️ Vacaciones / Ocio', 'value': 'a. Vacaciones/recreación/Ocio'},
                                {'label': '💼 Negocios', 'value': 'g. Negocios y motivos profesionales'},
                                {'label': '🏠 Visita Familiares', 'value': 'b. Visita a familiares y amigos'},
                                {'label': '🎓 Educación', 'value': 'c. Educación y formación'},
                                {'label': '🏥 Salud', 'value': 'd. Salud , Bienestar y atención médica'},
                                {'label': '🛍️ Compras', 'value': 'f. Compras'},
                                {'label': '⛪ Religión', 'value': 'e. Religión/Peregrinaciones'},
                                {'label': '🏭 Trabajo (Otra ciudad)', 'value': 'h. Trabajo remunerado en otra ciudad'},
                                {'label': '❓ Otro', 'value': 'i. Otro.'}
                            ],
                            style={"width": "100%"}
                        ),
                    ]),

                    # 3. Alojamiento
                    dmc.Col(span=12, children=[
                        dmc.Select(
                            id="input-alojamiento",
                            label="Tipo de Alojamiento",
                            description="¿Dónde se hospedará?",
                            value='a. Hotel',
                            icon=get_icon("radix-icons:home"),
                            data=[
                                {'label': '🏨 Hotel', 'value': 'a. Hotel'},
                                {'label': '🎒 Hostal', 'value': 'b. Hostal'},
                                {'label': '🏢 Apartahotel', 'value': 'c. Apartahotel'},
                                {'label': '📱 Airbnb / Plataforma', 'value': 'd. Inmueble de alquiler (pagos por plataforma dig)'},
                                {'label': '🏠 Casa Amigos/Familia', 'value': 'e. Casa propia, de familiares o amigos (sin pago)'},
                                {'label': '⛺ Otro', 'value': 'f. Otro'}
                            ],
                            style={"width": "100%"}
                        ),
                    ]),
                ]),

                dmc.Space(h=20),
                
                # Botón de Acción
                dmc.Button(
                    "Calcular Predicción",
                    id="btn-predecir",
                    variant="gradient",
                    gradient={"from": "teal", "to": "blue", "deg": 60},
                    fullWidth=True,
                    size="lg",
                    leftIcon=DashIconify(icon="fluent:calculator-20-regular")
                ),

                dmc.Divider(label="Resultado", labelPosition="center", my="lg"),

                # Área de Resultado
                dmc.LoadingOverlay(
                    html.Div(id="resultado-container", children=[
                        dmc.Alert(
                            title="Esperando datos...",
                            color="gray",
                            children="Configure los parámetros y presione calcular."
                        )
                    ])
                )
            ]),
            
            # Switch Modo Oscuro
            dmc.Space(h=20),
            dmc.Group(position="right", children=[
                dmc.Switch(
                    id="theme-switch",
                    size="lg",
                    onLabel=DashIconify(icon="radix-icons:moon", width=16),
                    offLabel=DashIconify(icon="radix-icons:sun", width=16),
                )
            ])
        ])
    ]
)

# ---------------------------------------------------------
# 3. LÓGICA (CALLBACKS)
# ---------------------------------------------------------

# Callback para cambiar tema (Light/Dark)
@app.callback(
    Output("mantine-provider", "theme"),
    Input("theme-switch", "checked"),
)
def update_theme(checked):
    return {"colorScheme": "dark" if checked else "light"}

# Callback Principal: Envía datos a la API y muestra respuesta
@app.callback(
    Output('resultado-container', 'children'),
    Input('btn-predecir', 'n_clicks'),
    State('input-duracion', 'value'),
    State('input-motivo', 'value'),
    State('input-alojamiento', 'value'),
    prevent_initial_call=True
)
def realizar_prediccion(n_clicks, duracion, motivo, alojamiento):
    # Crear el paquete de datos (JSON)
    payload = {
        "duracion": int(duracion),
        "motivo": motivo,
        "alojamiento": alojamiento
    }
    
    try:
        # LLAMADA A LA API (Microservicio)
        # Usamos f-string para insertar la URL configurada
        response = requests.post(f"{API_URL}/predict", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            valor = data["gasto_estimado"]
            
            # Alerta de Éxito
            return dmc.Alert(
                title="Estimación Exitosa",
                color="green",
                variant="filled",
                children=[
                    dmc.Group(position="apart", children=[
                        dmc.Text("Cálculo procesado vía API:"),
                        dmc.Badge("Estimación Exitosa", color="lime")
                    ]),
                    dmc.Space(h=10),
                    dmc.Text(f"${valor:,.0f} COP", size="xl", weight=700)
                ],
                icon=DashIconify(icon="game-icons:cash", height=30)
            )
        else:
            # Alerta de Error de la API (ej. 500)
            return dmc.Alert(
                title="Error en el Modelo", 
                color="red", 
                children=f"La API respondió con error {response.status_code}: {response.text}"
            )
            
    except Exception as e:
        # Alerta de Error de Conexión (ej. API apagada)
        return dmc.Alert(
            title="Error de Conexión", 
            color="red", 
            children=f"No se pudo conectar al servicio en {API_URL}. Detalles: {str(e)}"
        )

# Arranque del servidor
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
