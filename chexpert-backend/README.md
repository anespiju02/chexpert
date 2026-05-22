# CheXpert-v1.0-small Backend API

Este proyecto constituye el núcleo de inferencia y backend de procesamiento de imágenes para el sistema de diagnóstico automatizado de radiografías de tórax. Expone una API REST construida sobre **FastAPI** que utiliza un modelo **DenseNet121** preentrenado y ajustado mediante transferencia de aprendizaje (*Transfer Learning*) para clasificar simultáneamente 5 patologías torácicas clave.

---

## Arquitectura de Comunicación

El backend actúa de forma desacoplada al cliente web, procesando las solicitudes binarias a través de flujos de bytes eficientes:

[Cliente Angular 21] ───( POST /predict )───► [FastAPI Endpoint] ───► [Inferencia DenseNet121] ───► JSON Payload

## 🛠️ Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu sistema:
- **Python 3.12** o superior.
- **Antigravity IDE** configurado con el intérprete correspondiente al entorno virtual (`venv`).

---

## 💻 Instalación y Despliegue Local

Sigue estos pasos en la terminal integrada de tu IDE dentro del directorio `chexpert-backend/`:

1. **Crear el entorno virtual aislado:**
   ```bash
   python3 -m venv venv

2. **Activar el entorno virtual:**
   ```bash
   En Linux/macOS: source venv/bin/activate
   En Windows (PowerShell): .\venv\Scripts\activate

3. **Instalar dependencias del proyecto:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

4. **Colocación del Modelo:**
   Asegúrate de que tu archivo de pesos chexpert_densenet121.h5 exportado de Google Colab se encuentre ubicado exactamente en la raíz de este directorio o dentro de la ruta definida en main.py.

5. **Iniciar el servidor en modo desarrollo (Hot-Reload):**
   ```bash
   uvicorn app.main:app --reload --port 8000