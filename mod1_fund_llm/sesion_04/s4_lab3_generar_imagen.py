import os
import shutil

from dotenv import load_dotenv

# gradio_client
from gradio_client import Client 

ESPACIO = "jgomezz/generate-image"     # el nombre de SU Space
PROMPT = "Una dia de nieve en los andes de Perú"
DESTINO = "mod1_fund_llm/sesion_04/generadas/playa.png"

# Carga la clave de la API desde el archivo .env
cliente = Client(ESPACIO)

# Generar la imagen
ruta_temporal = cliente.predict(
    prompt=PROMPT,
    negative_prompt="",
    steps=9,
    seed=42,
    width=1024,
    height=1024,
    api_name="/generar",
)

# Guardar la imagen en el destino
shutil.copy(ruta_temporal, DESTINO)

# 
print("Imagen guardada en:", DESTINO)