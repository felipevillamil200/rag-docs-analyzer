¡Excelente Felipe! 🙌
Ya que tu proyecto ahora **sí incluye análisis automático de contratos + generación de reportes en PDF + mejoras visuales en Gradio**, actualicé tu README para que refleje todas estas capacidades reales (y no quede como “futuro” solamente).

---

## 📄 README.md actualizado

```markdown
# 📑 Chatbot RAG con Cerebras + Chroma + Gradio

Este proyecto implementa un **chatbot de Recuperación Aumentada con Generación (RAG)** que permite:

- Subir documentos en **PDF o DOCX**.
- **Extraer e indexar** el contenido en una base de datos vectorial (**Chroma**).
- Consultar los documentos en lenguaje natural.
- Obtener respuestas contextualizadas usando un **LLM de Cerebras**.
- Generar **resúmenes automáticos** de documentos.
- Realizar **análisis automático de contratos** (partes, monto, duración, jurisdicción, cláusula de terminación).
- Exportar resultados en **reportes PDF profesionales** usando `reportlab`.

---

## 🚀 Tecnologías utilizadas
- **LLM**: [Cerebras](https://inference.cerebras.net/) (API Key requerida).
- **Vector DB**: [Chroma](https://www.trychroma.com/) (open-source, corre localmente).
- **Framework RAG**: [LangChain](https://www.langchain.com/).
- **Procesamiento de documentos**: 
  - [PyPDF2](https://pypi.org/project/PyPDF2/) → PDFs.
  - [python-docx](https://pypi.org/project/python-docx/) → Word.
- **Interfaz de usuario**: [Gradio](https://www.gradio.app/).
- **Reportes**: [pandas](https://pandas.pydata.org/) + [reportlab](https://www.reportlab.com/).

---

## 📂 Estructura del proyecto

```

llm-rag-project/
│
├── app/
│   ├── **init**.py
│   ├── main.py              # Interfaz con Gradio
│   ├── document_loader.py   # Extraer texto de PDF/DOCX
│   ├── vector_store.py      # Manejo de Chroma (indexar/consultar)
│   └── rag_pipeline.py      # Conexión Chroma + Cerebras (RAG)
│
├── data/                    # Carpeta para documentos de prueba
│   ├── contrato_alquiler.pdf
│   └── acuerdo_confidencialidad.docx
│
├── requirements.txt
├── README.md
└── .env                     # Clave de API (no subir a GitHub)

````

---

## 🔑 Configuración de variables de entorno

Crea un archivo `.env` en la raíz del proyecto con tu API Key de **Cerebras**:

```env
CEREBRAS_API_KEY=tu_api_key_aqui
````

---

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/llm-rag-project.git
cd llm-rag-project
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# o
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la app

```bash
python -m app.main
```

### 5. Abrir en navegador

Gradio se levantará en:

```
http://127.0.0.1:7860
```

---

## 🧪 Uso

### 🔹 QA sobre documentos

1. Sube un documento PDF o DOCX.
2. Haz clic en **Indexar documento**.
3. Escribe una pregunta en lenguaje natural.
4. Recibe una respuesta contextualizada generada por **Cerebras + RAG**.

### 🔹 Resumen automático

* Haz clic en **Generar resumen** → el sistema devuelve un resumen en 5 puntos clave.

### 🔹 Análisis de contratos

* Haz clic en **Analizar contrato y generar reporte** → el sistema:

  * Extrae partes, monto, duración, jurisdicción y cláusula de terminación.
  * Muestra los resultados en una tabla interactiva.
  * Genera un **reporte PDF profesional**.

---

## 📌 Próximos pasos

* [ ] Permitir carga de **múltiples documentos** en la misma sesión.
* [ ] Agregar módulo de **evaluación automática de respuestas** (precisión/relevancia).
* [ ] Exponer la solución como **API REST (FastAPI)**.
* [ ] Desplegar en **Hugging Face Spaces** para demo pública.

---

## ⚠️ Notas

* Archivo `.env` a GitHub (Colocar tu API Key).
* Si quieres usar otro modelo distinto de Cerebras (ej: OpenAI, Hugging Face), puedes reemplazarlo en `rag_pipeline.py`.

---

## ✨ Autor

Proyecto desarrollado por **Felipe** como portafolio para vacantes en IA Generativa.

```

---


