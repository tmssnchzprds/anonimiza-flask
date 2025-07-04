import os
from flask import Flask, render_template, request, redirect, url_for, flash
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv

load_dotenv()  # Carga variables del .env

app = Flask(__name__)
app.secret_key = 'supersecret'  # Cambia esto en producción

# Configuración de Azure
form_recognizer_endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
form_recognizer_key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
text_analytics_endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
text_analytics_key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")

form_recognizer_client = DocumentAnalysisClient(
    endpoint=form_recognizer_endpoint,
    credential=AzureKeyCredential(form_recognizer_key)
)
text_analytics_client = TextAnalyticsClient(
    endpoint=text_analytics_endpoint,
    credential=AzureKeyCredential(text_analytics_key)
)

def extract_text_from_pdf(file):
    poller = form_recognizer_client.begin_analyze_document(
        "prebuilt-read", document=file
    )
    result = poller.result()
    pages = []
    for page in result.pages:
        page_text = ""
        for line in page.lines:
            page_text += line.content + "\n"
        pages.append(page_text)
    # Devuelve el texto concatenado de todas las páginas
    return "\n".join(pages)

def detect_pii(text):
    try:
        response = text_analytics_client.recognize_pii_entities([text], language="es")
        result = response[0]
        if not result.is_error:
            return result.entities
        else:
            print("Error en Text Analytics:", result.error)
            return []
    except Exception as e:
        print(f"Error detectando PII: {e}")
        return []

def highlight_pii(text, entities):
    # Resalta las entidades PII en el texto original
    # Vamos a ordenar las entidades por el índice de inicio, descendente, para evitar desplazar índices al insertar spans
    entities = sorted(entities, key=lambda e: e.offset, reverse=True)
    for entity in entities:
        start = entity.offset
        end = start + entity.length
        # Prepara el tooltip con la categoría
        replacement = (f'<span class="pii" style="background-color: yellow;" '
                       f'title="{entity.category}">{text[start:end]}</span>')
        text = text[:start] + replacement + text[end:]
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('document')
        if not file or file.filename == '':
            flash("Por favor, selecciona un archivo PDF.")
            return redirect(request.url)
        if not file.filename.lower().endswith('.pdf'):
            flash("Solo se permiten archivos PDF.")
            return redirect(request.url)
        try:
            text = extract_text_from_pdf(file)
            entities = detect_pii(text)
            text_highlighted = highlight_pii(text, entities)
            # Lista de entidades para mostrar como tabla (opcional)
            pii_list = [{
                "texto": e.text,
                "categoria": e.category,
                "subcategoria": getattr(e, "subcategory", ""),
                "confianza": round(e.confidence_score, 2)
            } for e in entities]
            return render_template('index.html', text=text_highlighted, pii_list=pii_list)
        except Exception as e:
            print(f"Error: {e}")
            flash("Ha ocurrido un error procesando el documento.")
            return redirect(request.url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
