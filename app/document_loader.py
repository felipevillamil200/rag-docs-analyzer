# app/document_loader.py
import PyPDF2
import docx
import os

def extraer_texto(file_path: str) -> str:
    """
    Extrae texto desde un archivo PDF o DOCX individual.
    """
    texto = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                try:
                    texto += page.extract_text() + "\n"
                except:
                    texto += "\n[⚠️ No se pudo extraer texto de una página]\n"
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for p in doc.paragraphs:
            texto += p.text + "\n"
    else:
        raise ValueError(f"Formato no soportado: {file_path}")
    
    # Limpieza de texto
    texto = " ".join(texto.split())
    return texto


def extraer_texto_multiple(files: list) -> str:
    """
    Procesa múltiples archivos y concatena su texto.
    """
    textos = []
    for f in files:
        if not os.path.exists(f):
            raise FileNotFoundError(f"Archivo no encontrado: {f}")
        textos.append(extraer_texto(f))
    return "\n\n".join(textos)
