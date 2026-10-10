import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

import logging


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


# Consulta sin tener la informacion de la politica de devolucion de la empresa TiendaYa

PREGUNTA = "¿Cuál es la política de devolución de la empresa TiendaYa para productos en oferta?"

'''
respuesta = llm.invoke(PREGUNTA)

print("Respuesta: " + respuesta.text)
'''

# Librería pypdf

from pypdf import PdfReader
from langchain_core.documents import Document


ARCHIVO = "mod2_prompt_app_llm/sesion_03/data/politica_tiendaya.pdf"

reader = PdfReader(ARCHIVO)
documentos = []

for i, pagina in enumerate(reader.pages):
    
    texto = pagina.extract_text()
    print(f"Página {i+1}: {texto[:100]}...")  # Muestra los primeros 100 caracteres de cada página

    doc = Document(page_content=texto, 
                   metadata={"pagina": i+1})
    
    documentos.append(doc)

print("Número de páginas procesadas: ", len(documentos))


# Segmentacion de documentos

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Se va a segmentar el documento en fragmetos con solapamientos

# Dividir el fragmentos de 500 carateres con un solapamiento de 50 caracteres

chunk_size = 500
chunk_overlap = 50

spliter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,  # fragmento de 500 caracteres
    chunk_overlap=chunk_overlap # solapamiento de 50 caracteres
)

fragmentos = spliter.split_documents(documentos)

print(f"{'chunk_size':>10} {'overlap':>8} {'fragmentos':>11}")
print(f"{chunk_size:>10} {chunk_overlap:>8} {len(fragmentos):>11}")


import math 

def similitud_coseno(v1, v2):
    """
    SIMILITUD COSENO = mide el angulo entre dos vectores.
    1.0  -> apuntan exactamente igual (muy parecidos)
    0.0  -> no tienen relacion
    Es la metrica que usan los LLMs reales para comparar embeddings.
    """
    producto_punto = sum(a * b for a, b in zip(v1, v2))
    norma1 = math.sqrt(sum(a * a for a in v1))
    norma2 = math.sqrt(sum(b * b for b in v2))
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return producto_punto / (norma1 * norma2)


from langchain_google_genai import GoogleGenerativeAIEmbeddings

MODEL_EMBEDDINGS = "gemini-embedding-001"  # Modelo de embeddings de Google GenAI

embeddings = GoogleGenerativeAIEmbeddings(model=MODEL_EMBEDDINGS)  # Modelo de embeddings de Google GenAI

PREGUNTA = "¿Cuál es la política de devolución de la empresa TiendaYa para productos en oferta?"

# Generar el vector de la pregunta
vector_pregunta = embeddings.embed_query(PREGUNTA)

print("Vector de la pregunta: ", vector_pregunta[:20], "...")  # Muestra los primeros 200 valores del vector


'''
for fragmento in fragmentos:
    print(fragmento.page_content[20], "...")  # Muestra los primeros 100 caracteres del fragmento
'''

vector_fragmentos = [ fragmento.page_content for fragmento in fragmentos]

#print(vector_fragmentos[:5])  # Muestra los primeros 5 fragmentos

vector_fragmentos_embeddings = embeddings.embed_documents(vector_fragmentos)

# print("Vector de embeddings de los fragmentos: ", vector_fragmentos_embeddings[:20], "...")  # Muestra los primeros 200 valores del vector



# Buscando similitudes entre el vector de la pregunta y los vectores de los fragmentos
similitudes = []

for i, fragmento in enumerate(vector_fragmentos_embeddings):
    similitud = similitud_coseno(vector_pregunta, fragmento)
    similitudes.append((similitud, i))
    #print(f"Fragmento {i+1}: Similitud = {similitud:.4f}")  

similitudes.sort(reverse=True)

print("Similitudes ordenadas de mayor a menor: ", similitudes[:5])  # Muestra las 5 similitudes más altas

for sim, i in similitudes[:3]:
    print(f"Fragmento {i+1}: Similitud = {sim:.4f}  pagina = {fragmentos[i].metadata['pagina']}  contenido = {fragmentos[i].page_content[:100]}...") 


from langchain_chroma import Chroma

# Borrar base de datos vectorial
Chroma( collection_name="tiendaYa_collection", 
        persist_directory="data/tiendaYa_db",
        embedding_function=embeddings).delete_collection()

# Persistencia de la base de datos de fragmentos en Chroma
base_datos = Chroma.from_documents(
    documents=fragmentos,
    embedding=embeddings,
    persist_directory="data/tiendaYa_db",
    collection_name="tiendaYa_collection",
    collection_metadata={"hnsw:space": "cosine"},
)


print(f"Fragmentos indexados: {base_datos._collection.count()}")

# Realizando una consulta a la base de datos de fragmentos en Chroma

resultado = base_datos.similarity_search(PREGUNTA, k=3)

for i, doc in enumerate(resultado):
    print(f"Resultado {i+1}: pagina = {doc.metadata['pagina']}  contenido = {doc.page_content[50]}...")


    # Realizando una consulta a la base de datos de fragmentos en Chroma

resultado = base_datos.similarity_search_with_score(PREGUNTA, k=3)

for i, (doc, score) in enumerate(resultado):
    print(f"Resultado {i+1}: pagina = {doc.metadata['pagina']}  contenido = {doc.page_content[50]}...  score = {score:.4f}")

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
