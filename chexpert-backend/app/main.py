from fastapi import FastAPI, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# 1. Configuración de Metadatos globales para la página de Swagger
app = FastAPI(
    title="Nodo de Inferencia CheXpert AI 🧬",
    description="""
    API REST de soporte diagnóstico computarizado para la evaluación simultánea de patologías torácicas.
    
    * **Filtro de Seguridad:** Implementa análisis de varianza cromática (RGB-Diff) para mitigar falsos positivos bloqueando muestras no médicas o capturas de pantalla.
    * **Core Neural:** Red DenseNet-121 optimizada mediante Transfer Learning.
    """,
    version="1.0.0",
    contact={
        "name": "Grupo 3",
        "email": "42702445@continental.edu.pe",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo .h5 entrenado en Colab
model = tf.keras.models.load_model('models/chexpert_densenet121.h5')
target_classes = ['Cardiomegaly', 'Edema', 'Consolidation', 'Atelectasis', 'Pleural Effusion']


# =========================================================
# 3. MODELOS DE MODELADO DE DATOS (Esquemas para Swagger)
# =========================================================
class PredictionItem(BaseModel):
    pathology: str = Field(..., description="Nombre de la condición clínica evaluada.", example="Pleural Effusion")
    probability: float = Field(..., description="Porcentaje inferido de probabilidad (Rango 0.0 a 1.0).", example=0.7337)

class DiagnosticSuccessResponse(BaseModel):
    success: bool = Field(True, description="Indica si la muestra pasó los controles médicos y fue procesada con éxito.")
    predictions: List[PredictionItem] = Field(..., description="Listado analítico con el reporte multietiqueta del modelo.")

class DiagnosticErrorResponse(BaseModel):
    success: bool = Field(False, description="Indica que la muestra fue rechazada por el sistema.")
    error: str = Field(..., description="Razón detallada del rechazo por parte del filtro cromático.", example="MUESTRA RECHAZADA: El sistema ha detectado artefactos cromáticos...")


# =========================================================
# 4. ENDPOINT DOCUMENTADO
# =========================================================
@app.post(
    "/predict",
    response_model=DiagnosticSuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluar Radiografía de Tórax",
    description="Recibe una placa digital monocromática en formato binario, ejecuta la validación de varianza cromática RGB y procesa la inferencia multietiqueta mediante DenseNet121.",
    responses={
        200: {
            "model": DiagnosticSuccessResponse,
            "description": "Inferencia completada con éxito. Devuelve el arreglo de probabilidades de las 5 patologías."
        },
        400: {
            "model": DiagnosticErrorResponse,
            "description": "Muestra inválida. La imagen no cumple con los requisitos de escala de grises o el formato está corrupto."
        }
    }
)
async def predict(file: UploadFile = File(..., description="Archivo binario de la imagen médica (JPG/PNG).")):
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    
    if img.mode != 'RGB':
        img_rgb = img.convert('RGB')
    else:
        img_rgb = img
        
    arr = np.array(img_rgb)
    
    # --- FILTRO DE SEGURIDAD (RGB-Diff) ---
    canal_r = arr[:, :, 0]
    canal_g = arr[:, :, 1]
    canal_b = arr[:, :, 2]
    
    diff_rg = np.abs(canal_r - canal_g).mean()
    diff_gb = np.abs(canal_g - canal_b).mean()
    
    # Si falla el filtro de color, devolvemos el esquema de error documentado
    if diff_rg > 5.0 or diff_gb > 5.0:
        return {
            "success": False,
            "error": "MUESTRA RECHAZADA: El sistema ha detectado artefactos cromáticos o color nativo. Por favor, suba una imagen médica válida en escala de grises (DICOM exportado a JPG/PNG)."
        }
    
    # --- INFERENCIA ---
    img_target = img_rgb.resize((224, 224))
    img_array = np.array(img_target) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)[0]
    
    payload = [
        {"pathology": target_classes[i], "probability": float(predictions[i])}
        for i in range(len(target_classes))
    ]
    
    return {"success": True, "predictions": payload}