
import ollama

MODELO = "qwen3.5:9b"

# URL donde esta corriendo el servidor de Ollama. Por defecto es "http://localhost:11434"
URL = "http://localhost:11434"
# URL = "https://canning-rerun-snowboard.ngrok-free.dev"


CLIENTE = ollama.Client(host=URL)


def preguntar(prompt, temperature=0, formato=None):

    respuesta = CLIENTE.chat(
        model=MODELO,
        think=False,                  # que no escriba su razonamiento
        format=formato,               # None = respuesta libre
        options={"temperature": temperature},
        messages=[{
            "role": "user",
            "content": prompt,
        }],
    )

    return (respuesta.message.content or "").strip()


if __name__ == "__main__":

    print(preguntar("¿Cuál es la capital de Perú?"))

