# Conectarse a un RAG - Qdrant

# ------------------------------------ 
### 1. Cargar el LLM
# ------------------------------------ 
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
import os

# Generar una funcion que obtenga el modelo LLM

def get_llm(prefix_model, temperature=0.9):
    """
    Obtiene un modelo de lenguaje (LLM) basado en el modelo especificado.

    Args:
        model (str): El nombre del modelo a utilizar.
        temperature (float, optional): La temperatura para la generación de texto. 
                                        Valores más altos producen respuestas más creativas.
                                        Valores más bajos producen respuestas más deterministas.
                                        Por defecto es 0.9.

    Returns:
        llm: Un objeto de modelo de lenguaje inicializado.
    """
    llm = init_chat_model(
                            model=prefix_model, 
                            # temperature=temperature
                          )
    return llm

# Configuración del modelo de lenguaje
load_dotenv()

prefix_model = os.getenv("PREFIX_MODEL")

# Obtención del modelo
llm = get_llm(prefix_model)


# ------------------------------------ 
### 2. Cargar el Embedding
# ------------------------------------ 

from langchain_google_genai import GoogleGenerativeAIEmbeddings

MODEL_EMBEDDINGS = "gemini-embedding-001"  # Modelo de embeddings de Google GenAI

embeddings = GoogleGenerativeAIEmbeddings(model=MODEL_EMBEDDINGS)  # Modelo de embeddings de Google GenAI



# ------------------------------------ 
### 3. Conectarse a la Base de datos Vectorial : Qdrant
# ------------------------------------ 

from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

QDRANT_URL = "https://canning-rerun-snowboard.ngrok-free.dev"
PORT=443

COLECCION = "politica_tiendaya_jgm"

cliente = QdrantClient(url=QDRANT_URL, port=PORT)

# Persistencia de la base de datos de fragmentos en Qdrant
base_datos = QdrantVectorStore(
    client=cliente,
    embedding=embeddings,
    collection_name=COLECCION
)


# ------------------------------------ 
### 4. Usar la consulta al LLM que tiene RAG
# ------------------------------------ 

from langchain_core.prompts import ChatPromptTemplate

PREGUNTA = "¿Cuál es la política de devolución de la empresa TiendaYa para productos en oferta?"

# 1. Base de datos vectorial 
retriever = base_datos.as_retriever(search_kwargs={"k": 3})

# 2. Prompt
prompt_rag = ChatPromptTemplate.from_template(
    """ 
    Eres el asistente de TiendaYa. Responde solo con el contexto; si no tiene la información, 
    indica que el documento no lo especifica. Cita la página entre paréntesis.
    
    Contexto:
           {contexto}
           
    Pregunta: 
           {pregunta}

    """
)

# 3. Buscar coincidencias en la base de datos vectorial
fragmentos = retriever.invoke(PREGUNTA)

contexto = ""
for f in fragmentos:
    contexto += f"[página {f.metadata['pagina']}] {f.page_content}\n\n"

# print(contexto)

# 4. Preparar el prompt final

prompt = prompt_rag.invoke({"contexto": contexto, 
                            "pregunta": PREGUNTA})

# print(prompt)

# 5. Usar el LLM

response = llm.invoke(prompt)

print(response.content)