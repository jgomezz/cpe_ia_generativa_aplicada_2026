import ollama

# 1) El modelo. Es el nombre exacto que sale con "ollama list".
MODELO = "qwen3:0.6b"

# 2) La pregunta. "role": "user" significa que la escribimos nosotros.
respuesta = ollama.chat(
    model=MODELO,
    messages=[
        {"role": "user", "content": "Cual es la capital de Perú?"}
    ],
)

# 3) La respuesta llega adentro de respuesta.message.content
print(respuesta.message.content)