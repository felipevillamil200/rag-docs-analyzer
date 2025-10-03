# app/vector_store.py
import chromadb
from langchain.text_splitter import CharacterTextSplitter

# Inicializar cliente Chroma local
def init_chroma():
    client = chromadb.Client()
    # Si ya existe, reutiliza la colección
    try:
        collection = client.get_collection("documentos")
    except:
        collection = client.create_collection("documentos")
    return collection

# Indexar texto en chunks
def indexar_texto(collection, texto, chunk_size=500, overlap=50):
    """
    Divide texto en fragmentos (chunks) y los agrega a la colección.
    """
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_text(texto)

    for i, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"chunk_{i}"])

    return len(chunks)

# Consultar Chroma para obtener contexto
def consultar(collection, pregunta, n=3):
    """
    Busca contexto relevante en Chroma para la pregunta.
    """
    try:
        results = collection.query(query_texts=[pregunta], n_results=n)
        if "documents" in results and len(results["documents"]) > 0:
            # Une los fragmentos en un solo contexto
            contexto = " ".join(results["documents"][0])
        else:
            contexto = ""
        return contexto
    except Exception as e:
        return f"❌ Error en consulta a Chroma: {str(e)}"
