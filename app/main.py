import os
import gradio as gr
import pandas as pd
from dotenv import load_dotenv
from app.document_loader import extraer_texto
from app.vector_store import init_chroma, indexar_texto, consultar
from app.rag_pipeline import preguntar_cerebras
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ===== Cargar variables de entorno =====
load_dotenv()

# ===== Inicializar Chroma =====
collection = init_chroma()

# ===== Funciones =====
def indexar_documento(file):
    if file is None:
        return "⚠️ No se ha subido ningún archivo."
    try:
        texto = extraer_texto(file)
        num_chunks = indexar_texto(collection, texto)
        return f"✅ Documento procesado e indexado en {num_chunks} fragmentos."
    except Exception as e:
        return f"❌ Error al procesar el documento: {str(e)}"

def preguntar(pregunta):
    if not pregunta.strip():
        return "⚠️ Por favor ingresa una pregunta."
    try:
        contexto = consultar(collection, pregunta)
        if not contexto:
            return "⚠️ No encontré información relevante en el documento."
        return preguntar_cerebras(pregunta, contexto)
    except Exception as e:
        return f"❌ Error al consultar: {str(e)}"

def resumir_documento():
    try:
        contexto = consultar(collection, "Resumen general del documento")
        if not contexto:
            return "⚠️ No hay documento indexado aún."
        return preguntar_cerebras("Resume este documento en 5 puntos clave.", contexto)
    except Exception as e:
        return f"❌ Error al generar resumen: {str(e)}"

def analizar_contrato():
    """
    Hace preguntas predefinidas al LLM y genera un reporte tabular + PDF
    """
    preguntas_clave = {
        "Partes": "¿Quiénes son las partes involucradas?",
        "Monto": "¿Cuál es el monto total o mensual?",
        "Duración": "¿Cuál es la duración o fechas del contrato?",
        "Jurisdicción": "¿Cuál es la jurisdicción o lugar aplicable?",
        "Cláusula de terminación": "¿Qué dice la cláusula de terminación?"
    }

    resultados = {}
    for clave, q in preguntas_clave.items():
        contexto = consultar(collection, q)
        if contexto:
            resultados[clave] = preguntar_cerebras(q, contexto)
        else:
            resultados[clave] = "No encontrado"

    # Mostrar tabla en Gradio
    df = pd.DataFrame(list(resultados.items()), columns=["Elemento", "Respuesta"])

    # Generar PDF con reportlab (texto ajustado a celdas)
    pdf_file = "reporte_contrato.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(
        name="CellStyle",
        fontSize=10,
        leading=12,
        wordWrap='CJK'  # permite ajuste automático de línea
    )

    elements = []
    elements.append(Paragraph("Reporte de Análisis de Contrato", styles['Title']))

    data = [["Elemento", "Respuesta"]]
    for clave, valor in resultados.items():
        data.append([Paragraph(clave, cell_style), Paragraph(valor, cell_style)])

    table = Table(data, colWidths=[120, 400])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)

    return df, pdf_file

# ===== Interfaz Gradio =====
with gr.Blocks() as demo:
    gr.Markdown("## 📑 Chatbot RAG con Cerebras + Chroma (Mejorado)")

    with gr.Row():
        file_input = gr.File(label="Sube un PDF o DOCX", type="filepath")
        estado = gr.Textbox(label="Estado", lines=2)
    indexar_btn = gr.Button("Indexar documento")
    indexar_btn.click(indexar_documento, inputs=file_input, outputs=estado)

    with gr.Row():
        pregunta_input = gr.Textbox(label="Pregunta")
        respuesta_output = gr.Textbox(label="Respuesta", lines=8, show_copy_button=True)
    preguntar_btn = gr.Button("Preguntar")
    preguntar_btn.click(preguntar, inputs=pregunta_input, outputs=respuesta_output)

    gr.Markdown("### 📌 Funciones avanzadas")
    resumen_btn = gr.Button("Generar resumen")
    resumen_output = gr.Textbox(label="Resumen", lines=10, show_copy_button=True)
    resumen_btn.click(resumir_documento, outputs=resumen_output)

    analisis_btn = gr.Button("Analizar contrato y generar reporte")
    analisis_tabla = gr.DataFrame(headers=["Elemento", "Respuesta"], wrap=True, interactive=False)
    analisis_pdf = gr.File(label="Reporte PDF generado")
    analisis_btn.click(analizar_contrato, outputs=[analisis_tabla, analisis_pdf])

demo.launch()
