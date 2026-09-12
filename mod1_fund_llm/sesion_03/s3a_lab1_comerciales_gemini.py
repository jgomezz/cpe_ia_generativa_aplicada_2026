"""
Lab 1 (version paso a paso): GEMINI POR HTTP
======================================================
Esta es la MISMA leccion que s3a_lab1_comerciales_http.py (llamar a una
API sin librerias, solo con HTTP), pero escrita de la forma mas
explicita posible: SIN diccionario de proveedores y SIN una funcion
generica que elige el formato por ustedes. Cada proveedor tiene su
propia funcion, de arriba a abajo, para poder leerla sin saltar a
ningun otro lado del archivo.

La idea de fondo es siempre la misma en los tres:

    1) armar la URL             -> a donde se manda la peticion
    2) armar las cabeceras      -> ahi va la CLAVE (la contraseña de la cuenta)
    3) armar el cuerpo (JSON)   -> el modelo y la pregunta
    4) mandar la peticion HTTP  -> con la libreria urllib, sin instalar nada
    5) leer la respuesta (JSON) -> el texto que contesto y los tokens que costo

Los tres proveedores solo cambian en DETALLES de la forma: como se
llama la cabecera de la clave, como se llama el campo del texto en la
respuesta. Verlos por separado, uno por uno, ayuda a notar justo esas
diferencias.

Version "open source": s3a_lab1_open_source_http_paso_a_paso.py hace
lo mismo con un modelo que corre en su propia maquina (Ollama).

Requiere: python-dotenv y un archivo .env con al menos una de las tres
claves (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY).
Ejecutar desde la raiz del repositorio.
"""

import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

# La instruccion que le damos al modelo antes de la pregunta del usuario.
SISTEMA = "Responde en español, de forma breve y directa."

# La pregunta que le vamos a hacer a los tres, para poder comparar sus respuestas.
PREGUNTA = "En que año se fundo la ciudad de Lima y quien la fundo? Responde en una sola frase."


def enviar_peticion_post(url, cabeceras, cuerpo):
    """Esta funcion la usan los tres proveedores: es lo unico que hace
    una libreria de API por dentro. Manda un JSON por HTTP POST y
    devuelve el JSON que responde el servidor.

    Si algo sale mal (clave invalida, sin credito, modelo que no
    existe), el servidor responde con un codigo de error (por ejemplo
    401 o 429) y aqui lo convertimos en un mensaje de error legible.
    """
    # el cuerpo es un diccionario de Python; hay que convertirlo a texto JSON y luego a bytes
    cuerpo_como_texto = json.dumps(cuerpo)
    cuerpo_en_bytes = cuerpo_como_texto.encode("utf-8")

    # todas las peticiones avisan que mandan JSON; ademas van las cabeceras propias del proveedor
    cabeceras_completas = {"Content-Type": "application/json"}
    for nombre_de_cabecera in cabeceras:
        cabeceras_completas[nombre_de_cabecera] = cabeceras[nombre_de_cabecera]

    peticion = urllib.request.Request(
        url,
        data=cuerpo_en_bytes,
        method="POST",
        headers=cabeceras_completas,
    )

    try:
        with urllib.request.urlopen(peticion, timeout=180) as respuesta_http:
            texto_de_respuesta = respuesta_http.read()
            return json.loads(texto_de_respuesta)
    except urllib.error.HTTPError as error:
        cuerpo_del_error = error.read().decode("utf-8", errors="replace")
        mensaje = f"HTTP {error.code} {error.reason}: {cuerpo_del_error[:200]}"
        raise RuntimeError(mensaje) from None

# ============================================================
# GEMINI (Google)
# ===============================================


#def preguntar_gemini(pregunta, modelo="gemma-4-31b-it"):
#def preguntar_gemini(pregunta, modelo="gemma-4-26b-a4b-it"):
#def preguntar_gemini(pregunta, modelo="gemini-3.1-flash-lite"):
#def preguntar_gemini(pregunta, modelo="gemini-3.5-flash"):
#def preguntar_gemini(pregunta, modelo="gemini-3.6-flash"):
#def preguntar_gemini(pregunta, modelo="gemini-3.7-flash"):

def preguntar_gemini(pregunta, modelo="gemini-3.5-flash-lite"):
    """Le hace una pregunta a Gemini (Google) y devuelve el texto de la
    respuesta, los tokens de entrada y los tokens de salida.

    Aqui hay tres diferencias grandes con los otros dos:
      - el nombre del modelo va DENTRO de la URL, no en el cuerpo
      - la clave va en la cabecera "x-goog-api-key"
      - cada mensaje se llama "content" y el texto va adentro de una
        lista "parts"
    """
    clave = os.environ.get("GEMINI_API_KEY", "")
    if not clave:
        raise RuntimeError("Falta GEMINI_API_KEY en el archivo .env")

    # 1) URL: el modelo forma parte de la direccion
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

    # 2) cabeceras
    cabeceras = {
        "x-goog-api-key": clave,
    }

    # 3) cuerpo: la instruccion de sistema va aparte, y el mensaje del
    #    usuario se envuelve en "content" -> "parts" -> "text"
    cuerpo = {
        "system_instruction": {
            "parts": [{"text": SISTEMA}],
        },
        "contents": [
            {"role": "user", "parts": [{"text": pregunta}]},
        ],
    }

    # 4) mandar
    respuesta = enviar_peticion_post(url, cabeceras, cuerpo)

    # 5) leer: el texto esta en "candidates" -> primer candidato -> "content" -> "parts" -> primera parte
    texto = respuesta["candidates"][0]["content"]["parts"][0]["text"]
    tokens_entrada = respuesta["usageMetadata"]["promptTokenCount"]
    tokens_salida = respuesta["usageMetadata"]["candidatesTokenCount"]

    return texto, tokens_entrada, tokens_salida


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    load_dotenv()

    print("Pregunta :", PREGUNTA)

    print("\n=== Gemini (Google) ===")
    try:
        texto, tokens_entrada, tokens_salida = preguntar_gemini(PREGUNTA)
        print(texto)
        print(f"tokens de entrada: {tokens_entrada}  tokens de salida: {tokens_salida}")
    except Exception as error:
        print("ERROR:", error)

    