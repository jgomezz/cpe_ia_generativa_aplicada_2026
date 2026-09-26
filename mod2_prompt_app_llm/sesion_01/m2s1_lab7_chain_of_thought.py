from prompting_base import preguntar
# ----- CASO 1 : Respuesta directa ----

MENSAJE = """
Un cliente de TiendaYa compró 3 polos a S/ 45 cada uno y 2 pantalones a S/ 89 cada uno.
Devolvió 1 polo y 1 pantalón. El envío (S/ 15) no es reembolsable.
¿Cuánto se le reembolsa?

Responde solo con el monto.
"""
print("=============================")
print("MENSAJE:", MENSAJE)
print("-------------------")
print("RESULTADO:" ,preguntar(MENSAJE))

# ----- CASO 2 : Detalle del paso a paso ----

MENSAJE_CoT = """
Un cliente de TiendaYa compró 3 polos a S/ 45 cada uno y 2 pantalones a S/ 89 cada uno.
Devolvió 1 polo y 1 pantalón. El envío (S/ 15) no es reembolsable.
¿Cuánto se le reembolsa?

Detalla el paso a paso e indica el monto al final.

"""
print("=============================")
print("MENSAJE_CoT:", MENSAJE_CoT)
print("-------------------")
print("RESULTADO:" ,preguntar(MENSAJE_CoT))
