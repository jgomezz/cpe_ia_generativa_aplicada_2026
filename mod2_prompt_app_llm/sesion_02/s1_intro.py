import logging
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env   
load_dotenv()  

# Configuración del nivel de logging para el modelo de lenguaje
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

# Configuración del modelo de lenguaje
prefix_model = os.getenv("PREFIX_MODEL")

# Inicialización del modelo de lenguaje
llm = init_chat_model(model=prefix_model)

# Uso del modelo de lenguaje
response = llm.invoke("Cual es la capital de Perú?")

# Imprime la respuesta del modelo
print(response.text)


