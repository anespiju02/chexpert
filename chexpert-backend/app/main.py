import os
import builtins
from typing import Annotated
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image
import io

app = FastAPI(title="PlacaAI - API Multimodal")

# Configuración de CORS para conectar con Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# PARCHE DE APERTURA VIRTUAL (Para asegurar la estabilidad del modelo .h5)
# ------------------------------------------------------------------------------
open_original = builtins.open
def open_interceptor(file, *args, **kwargs):
    if isinstance(file, str) and "CheXpert-v1.0-small/" in file:
        # Si el modelo guardó referencias internas rígidas, las redirigimos a una ruta local o limpia
        sub_ruta = file.split("CheXpert-v1.0-small/", 1)[1]
        file = os.path.join("./", sub_ruta)
    return open_original(file, *args, **kwargs)
builtins.open = open_interceptor

# Carga del modelo híbrido multimodal entrenado
MODEL_PATH = "models/chexpert_multimodal_sex.h5"
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Modelo Multimodal cargado exitosamente.")
else:
    print(f"❌ Alerta: No se encontró el archivo {MODEL_PATH}")

# Lista de clases objetivo del dataset CheXpert
TARGET_CLASSES = ['Cardiomegaly', 'Edema', 'Consolidation', 'Atelectasis', 'Pleural Effusion']

# ------------------------------------------------------------------------------
# ENDPOINT MODIFICADO: AHORA RECIBE EL GÉNERO COMO UN FORM FIELD
# ------------------------------------------------------------------------------
@app.post("/api/v1/predict")
async def predict(
    file: Annotated[UploadFile, File(...)],
    genero: Annotated[str, Form(...)] # Recibe 'Male', 'Female' o 'Unknown' desde el Front
):
    # 1. Validar y procesar la variable demográfica (Género)
    if genero == 'Masculino':
        sex_numeric = 1.0
    elif genero == 'Femenino':
        sex_numeric = 0.0
    else:
        sex_numeric = 0.5 # Punto neutral de incertidumbre

    try:
        # 2. Leer e inspeccionar la imagen médica recibida
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # 3. Preprocesamiento de imagen idéntico al entrenamiento (224x224 y rescale 1/255)
        image = image.resize((224, 224))
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_tensor = np.expand_dims(img_array, axis=0) # Formato (1, 224, 224, 3)

        # 4. Preparar el formato de entrada para la Red Multimodal
        # Pasamos un diccionario cuyas llaves coincidan con los nombres de las capas Input de Keras
        input_genero_tensor = np.array([[sex_numeric]], dtype=np.float32) # Formato (1, 1)
        
        entradas_modelo = {
            "input_imagen": img_tensor,
            "input_genero": input_genero_tensor
        }

        # 5. Inferencia / Predicción
        predictions = model.predict(entradas_modelo)[0]

        # 6. Estructurar la respuesta clínica para el Frontend
        resultados = {
            target: float(predictions[i]) 
            for i, target in enumerate(TARGET_CLASSES)
        }
        
        return {
            "status": "success",
            "metadata_procesada": {"genero_recibido": genero, "valor_numerico": sex_numeric},
            "predictions": resultados
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")