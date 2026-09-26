
from prompting_base import preguntar

# ----- CASO 1 ----

MENSAJE = """
El pedido llegó tres días tarde y la caja venía golpeada. ¿Qué opinas?
"""
print("MENSAJE:", MENSAJE)
print("-------------------")
print("RESULTADO:" ,preguntar(MENSAJE))


# ----- CASO 2 ----


MENSAJE_ESTRUCTURADO = """

Eres el sistema de clasificación de TiendaYa.
Clasifica el sentimiento del siguiente mensaje de un cliente.

Mensaje:
\"\"\"El pedido llegó tres días tarde y la caja venía golpeada.\"\"\"

Responde con una sola palabra: positivo, negativo o neutral.

"""

print("MENSAJE_ESTRUCTURADO:", MENSAJE_ESTRUCTURADO)
print("-------------------")
print("RESULTADO:", preguntar(MENSAJE_ESTRUCTURADO))

