
from prompting_base import CLIENTE, MODELO

SYSTEM_PROMPT = """
Eres el asistente de reclamos de TiendaYa.
- Solo respondes sobre pedidos, envíos y devoluciones.
- Si te preguntan otra cosa, responde exactamente: "Solo puedo ayudarle con sus pedidos."
- Nunca prometas reembolsos: indica que un agente lo revisará.
- Máximo 3 líneas por respuesta. Trata de usted.
"""
USER_PROMPT = "Mi pedido llegó roto."


def preguntar(mensaje, temperature=0, formato=None):

    respuesta = CLIENTE.chat(
        model=MODELO,
        think=False,                  # que no escriba su razonamiento
        format=formato,               # None = respuesta libre
        options={"temperature": temperature},
        messages=mensaje,
    )

    return (respuesta.message.content or "").strip()

if __name__ == "__main__":
    
    mensaje = [
                {"role": "system", 
                 "content": SYSTEM_PROMPT},
                {"role": "user", 
                 "content": USER_PROMPT},
    ]

    response = preguntar(mensaje)

    print(response)




