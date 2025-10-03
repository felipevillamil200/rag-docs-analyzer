# app/rag_pipeline.py
import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar cliente Cerebras
api_key = os.environ.get("CEREBRAS_API_KEY")
if not api_key:
    raise ValueError("❌ No se encontró la variable CEREBRAS_API_KEY. Revisa tu archivo .env")

client = Cerebras(api_key=api_key)

def preguntar_cerebras(pregunta, contexto, role="Eres un asistente experto en análisis de documentos."):
    """
    Usa el modelo Cerebras para responder preguntas
    con contexto recuperado desde Chroma.
    Permite cambiar el rol (ej. resumen, análisis, QA).
    """
    try:
        stream = client.chat.completions.create(
            model="qwen-3-235b-a22b-instruct-2507",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {pregunta}"}
            ],
            stream=True,
            max_completion_tokens=500,
            temperature=0.2
        )

        respuesta = ""
        for chunk in stream:
            respuesta += chunk.choices[0].delta.content or ""
        return respuesta.strip()
    except Exception as e:
        return f"❌ Error al consultar Cerebras: {str(e)}"
