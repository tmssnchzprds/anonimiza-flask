# PoC Plataforma de Anonimización de Documentos con Flask y Azure AI

## Descripción

Esta es una prueba de concepto (PoC) para una plataforma web que permite subir documentos PDF (incluyendo escaneos, manuscritos e imágenes) y obtener el texto extraído con la información personal identificable (PII) resaltada y clasificada.

El proyecto usa servicios de Azure AI para:

- Extraer texto mediante **Azure Document Intelligence (Form Recognizer)**
- Detectar y clasificar datos sensibles (PII) con **Azure AI Language (Text Analytics)**

La aplicación está desarrollada con **Flask** en Python, con una interfaz sencilla para cargar documentos y visualizar el resultado resaltado.

---

## Arquitectura propuesta

Usuario --> Flask (Frontend Web) --> Azure Document Intelligence (OCR)
                                       |
                                       v
                             Azure Text Analytics (PII Detection)
                                       |
                                       v
                        Flask (procesa resultado y genera vista)
                                       |
                                       v
                                Navegador del Usuario
El usuario sube un PDF a la aplicación Flask mediante formulario web.

Flask envía el documento a Azure Document Intelligence para extraer texto (OCR), capaz de manejar texto impreso y manuscrito con alta precisión.

El texto extraído se envía al servicio Azure Text Analytics para detectar PII, como nombres, números de teléfono, emails, documentos de identidad, etc.

Flask recibe la respuesta con las entidades PII identificadas y genera una vista HTML donde el texto se muestra con las PII resaltadas (por ejemplo, fondo amarillo) y clasificadas con etiquetas visibles o tooltips.

El usuario puede revisar el texto resaltado y ver un listado con las entidades encontradas para facilitar la validación y posibles intervenciones manuales.

---

## Características principales

- Extracción automática de texto vía OCR desde PDFs.
- Detección y clasificación de PII (nombres, emails, teléfonos, DNI, direcciones, etc.).
- Visualización web con PII resaltada y etiquetada.
- Listado tabulado de entidades detectadas con nivel de confianza.
- Código modular y preparado para extensiones futuras (anonimización, multi-idioma, etc.).
- Uso de variables de entorno para gestionar credenciales Azure.
- Manejo básico de errores y validación de archivos.

---

## Servicios Azure usados

**Azure Document Intelligence (Form Recognizer)**
- Servicio especializado en extracción de texto y estructura desde documentos PDF e imágenes.
- Soporta documentos escaneados e incluso manuscritos con buena precisión.
- Devuelve texto con estructura, líneas y posiciones (bounding boxes).
- Fácil integración con SDK Python y REST API.
- Coste: por página procesada, con nivel gratuito para pruebas.
- Alta calidad OCR para documentos en español.
**Azure AI Language (Text Analytics) – Detección de PII**
- Servicio de Named Entity Recognition especializado en información personal sensible.
- Detecta y clasifica datos como nombres, direcciones, emails, teléfonos, DNI, números bancarios, etc.
- Devuelve posiciones e identificadores para fácil resaltado en texto.
- Incluye modelo preentrenado listo para usar sin necesidad de entrenamiento adicional.
- Soporte para español y otros idiomas.
- Coste: por número de textos/análisis, con nivel gratuito para pruebas.
- Alta precisión para la mayoría de categorías comunes.

## Requisitos

- Python 3.9 o superior
- Cuenta Azure activa con recursos:
  - Azure AI Document Intelligence (Form Recognizer)
  - Azure AI Language (Text Analytics)

---

## Flujo

- Subida y validación del PDF.
- Extracción de texto por Azure OCR.
- Análisis de PII en el texto extraído.
- Construcción del texto resaltado con etiquetas HTML.
- Renderizado web con texto e información adicional.

---

## Instalación

1. Clona este repositorio:

git clone https://github.com/tmssnchzprds/anonimiza-flask.git
cd anonimiza-flask

2. Asegúrate de tener tu archivo .env con las claves y endpoints de Azure.

3. Instala dependencias con pip install -r requirements.txt.

3. Lanza la app:

python app.py

4. Accede a http://localhost:5000 en tu navegador, sube un PDF y revisa el texto extraído y la información PII resaltada y clasificada.

---