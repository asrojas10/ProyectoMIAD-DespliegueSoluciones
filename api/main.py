from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI(title="API Gasto Turístico")

# 1. Cargar el modelo al iniciar
# Usamos una ruta relativa segura para Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "modelo_gasto_turistico1.pkl")

try:
    with open(MODEL_PATH, 'rb') as f:
        modelo = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError(f"No se encontró el modelo en {MODEL_PATH}")

# 2. Definir la estructura de los datos que van a llegar
class TravelerInput(BaseModel):
    duracion: int
    motivo: str
    alojamiento: str

# 3. Columnas exactas que espera tu modelo (tomadas de tu entrenamiento anterior)
COLUMNAS_MODELO = [
    'duracion_estadia', 
    'P_103_b. Visita a familiares y amigos', 'P_103_c. Educación y formación', 
    'P_103_d. Salud , Bienestar y atención médica', 'P_103_e. Religión/Peregrinaciones', 
    'P_103_f. Compras', 'P_103_g. Negocios y motivos profesionales', 
    'P_103_h. Trabajo remunerado en otra ciudad', 'P_103_i. Otro.', 
    'P_107_b. Hostal', 'P_107_c. Apartahotel', 
    'P_107_d. Inmueble de alquiler (pagos por plataforma dig)', 
    'P_107_e. Casa propia, de familiares o amigos (sin pago)', 'P_107_f. Otro'
]

@app.post("/predict")
def predict_expense(data: TravelerInput):
    try:
        # A. Crear DataFrame base con ceros
        input_dict = dict.fromkeys(COLUMNAS_MODELO, 0)
        
        # B. Llenar valor numérico
        input_dict['duracion_estadia'] = data.duracion
        
        # C. One-Hot Encoding Manual (Mapeo)
        # Construimos las llaves dinámicamente según lo que llegue
        col_motivo = f"P_103_{data.motivo}"
        if col_motivo in input_dict:
            input_dict[col_motivo] = 1
            
        col_alojamiento = f"P_107_{data.alojamiento}"
        if col_alojamiento in input_dict:
            input_dict[col_alojamiento] = 1

        # D. Predecir
        df_input = pd.DataFrame([input_dict])
        prediction = modelo.predict(df_input)[0]
        
        return {"gasto_estimado": float(prediction)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))