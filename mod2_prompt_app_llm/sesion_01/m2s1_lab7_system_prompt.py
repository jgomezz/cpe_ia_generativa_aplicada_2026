
from prompting_base import CLIENTE, MODELO

SYSTEM_PROMPT = """
Eres el asistente de reclamos de TiendaYa.
- Solo respondes sobre pedidos, envíos y devoluciones.
- Siempre pide el número de pedido para poder ayudarle.
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

    # Turno 1

    mensaje = [
                {"role": "system", 
                 "content": SYSTEM_PROMPT},
                {"role": "user", 
                 "content": USER_PROMPT},
    ]

    respuesta = preguntar(mensaje)
    print("Respuesta del turno 1:")
    print(respuesta)

    # Turno 2

    mensaje = [
                {"role": "system", 
                 "content": SYSTEM_PROMPT},
                {"role": "assistant", 
                 "content": respuesta},
                {"role": "user", 
                 "content": "Es el pedido 48213. ¿Me devuelven el dinero?"},
    ]

    respuesta_final = preguntar(mensaje)

    print("Respuesta del turno 2:")
    print(respuesta_final)




