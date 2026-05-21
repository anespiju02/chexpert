# PlacaAI: Sistema Modular de Soporte Diagnóstico para Radiografías de Tórax 🧬

Este repositorio contiene la arquitectura completa de **PlacaAI**, un prototipo comercial y de investigación clínica desarrollado para la detección simultánea de 5 patologías torácicas clave. El sistema utiliza técnicas de Aprendizaje Profundo (*Deep Learning*) alimentadas por el corpus **CheXpert** de la Universidad de Stanford, integrando políticas proactivas de seguridad informática y un diseño de interfaz modular de alta fidelidad.

---

## 🏛️ Arquitectura General del Sistema

El proyecto está diseñado bajo un enfoque de **Monorrepo Desacoplado**, lo que garantiza que las reglas de negocio del modelo de IA y la interfaz de usuario web escalen de forma independiente sin pisar sus dependencias:
[ Frontend: Angular 21 ] ────( POST Multipart /predict )────► [ Backend: FastAPI ] ───► [ Inferencia DenseNet121 ]
* **`chexpert-backend/`**: API REST de alto rendimiento montada en **FastAPI (Python 3.12)**. Se encarga de la validación cromática de seguridad de la muestra y de la ejecución de tensores en TensorFlow.
* **`chexpert-frontend/`**: Aplicación cliente médica estructurada en **Angular 21**. Construida con componentes *Standalone*, manejo de estado reactivo mediante *Signals* y carga perezosa (*Lazy Loading*).

---

## 🛡️ Capa de Seguridad Activa (Mitigación de Falsos Positivos)

Para garantizar un entorno comercial seguro, el backend implementa un algoritmo de **Análisis de Varianza Cromática (RGB-Diff)**. Las radiografías médicas digitales nativas son monocromáticas; si un usuario intenta subir una captura de pantalla del navegador, una fotografía del entorno o un archivo corrupto a color, el sistema detectará el diferencial cromático en los píxeles y **bloqueará la inferencia antes de que llegue a la red neuronal**, notificando el rechazo en la interfaz gráfica.

---

## 🚀 Guía de Despliegue Rápido (Localhost)

Para levantar el ecosistema completo en tu entorno de desarrollo, abre tu IDE y ejecuta los siguientes bloques en terminales independientes:

### 1. Levantar el Servidor de Inferencia (Backend)
```bash
cd chexpert-backend
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
La documentación interactiva de Swagger se autogenerará en: http://localhost:8000/docs

2. Levantar el Panel Clínico (Frontend)
cd chexpert-frontend
npm install               # Instalar módulos de Node la primera vez
ng serve --open

El sistema se compilará y abrirá automáticamente en tu navegador bajo la URL: http://localhost:4200

💾 Descarga de los Pesos del Modelo (.h5)
Por motivos de optimización y políticas de almacenamiento de Git (restricción de archivos mayores a 100 MB), los pesos de la red DenseNet-121 entrenada (chexpert_densenet121.h5) están excluidos del control de versiones mediante el archivo .gitignore.

Para poner a funcionar el sistema:

Descarga el archivo del modelo desde nuestro almacenamiento seguro en el siguiente enlace: [INSERTAR_AQUÍ_TU_ENLACE_A_GOOGLE_DRIVE].

Copia el archivo chexpert_densenet121.h5 y pégalo directamente en la raíz de la carpeta chexpert-backend/.

📋 Ficha Técnica Breve
Arquitectura Base: DenseNet-121 (Transfer Learning + Fine Tuning).

Dataset: CheXpert v1.0 small (Stanford ML Group) - 224,316 imágenes.

Manejo de Incertidumbre: Estrategia U-Zeros (Mapeo de valores -1 a 0).

Patologías Evaluadas: Cardiomegalia, Edema, Consolidación, Atelectasia y Efusión Pleural.

---

### Conclusión
Con este archivo en la raíz, tu repositorio ganará un peso académico y profesional tremendo. Cualquier jurado o revisor sabrá de inmediato de qué trata tu tesis, qué tecnologías innovadoras usaste (como Angular 21 y FastAPI) y cómo clonar el proyecto en su máquina sin perderse en el intento.
