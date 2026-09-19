import os

from dotenv import load_dotenv

# Instalar la libreria google-genai con:
from google import genai # 
from google.genai import types

# El modelo y la foto que le vamos a comprender.
#MODELO = "gemini-3.7-flash"
MODELO = "gemini-3.5-flash-lite"
IMAGEN = "mod1_fund_llm/sesion_04/imagenes/title.png"

# Carga la clave de la API desde el archivo .env
load_dotenv()
cliente = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Leer la imagen
bytes_de_la_imagen = open(IMAGEN, "rb").read()
imagen = types.Part.from_bytes(data=bytes_de_la_imagen, mime_type="image/png")

# Hacer la pregunta a Gemini (Google)
respuesta = cliente.models.generate_content(
    model=MODELO,
    contents=[imagen, "Dame el texto de la imagen."],
)

# Mostrar la respuesta
print(respuesta.text)


