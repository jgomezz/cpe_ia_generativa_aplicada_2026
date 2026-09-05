"""
Fase 1: ATENCION - la idea estrella del Transformer
======================================================
En la sesion 1 el modelo miraba las ultimas letras del contexto
y todas pesaban igual. Pero en una frase no todas las palabras
importan igual: en "el gato come pescado", para entender "come"
importan mucho "gato" (quien come) y "pescado" (que come),
y muy poco "el".

ATENCION = dejar que cada palabra DECIDA cuanto mirar a las demas:

    1) COMPARAR su vector con el de cada palabra de la frase
    2) REPARTIR su atencion segun esos puntajes (todo suma 100%)
    3) MEZCLAR los vectores de la frase segun lo repartido

El resultado: cada palabra sale con un vector nuevo que ya lleva
informacion de su contexto. Un Transformer (la arquitectura de
GPT, Claude, Gemini...) hace basicamente esto, miles de veces.

Cada funcion es un bloque conceptual:

    comparar()          -> que tanto encajan dos palabras
    repartir_atencion() -> puntajes -> porcentajes que suman 1
    atender()           -> mezclar los vectores segun los porcentajes
"""

import math

# Embeddings de juguete (la idea del lab 5 de la sesion 1):
# cada palabra es una lista de numeros. Aqui los escribimos A MANO
# y con dimensiones legibles, para poder VER lo que pasa.
#              animal  comida  accion  articulo
EMBEDDINGS = {
    "el":      [0.0,    0.0,    0.0,    1.0],  # x [0.0,    0.0,    0.0,    1.0]
    "gato":    [1.0,    0.0,    0.2,    0.0],  # x [0.0,    0.0,    0.0,    1.0]
    "come":    [0.3,    0.6,    1.0,    0.0],  # x [0.0,    0.0,    0.0,    1.0]
    "pescado": [0.0,    1.0,    0.0,    0.0],  # x [0.0,    0.0,    0.0,    1.0]
}

def comparar(v1, v2):
    """COMPARAR = multiplicar posicion por posicion y sumar.
    Da un numero alto si los vectores 'encajan'.
    (Es primo de la similitud coseno del lab 5 de la sesion 1.)"""
    return sum(a * b for a, b in zip(v1, v2))


def repartir_atencion(puntajes):
    """REPARTIR = convertir puntajes en porcentajes que suman 1.
    El puntaje mas alto se lleva la mayor tajada.
    (Los tecnicos llaman 'softmax' a esta operacion.)"""
    mayor = max(puntajes)
    exps = [math.exp(p - mayor) for p in puntajes]
    suma = sum(exps)
    return [e / suma for e in exps]


def atender(palabra, frase):
    """ATENDER = los 3 pasos: comparar -> repartir -> mezclar.
    Devuelve los porcentajes y el nuevo vector de la palabra."""
    mi_vector = EMBEDDINGS[palabra]

    puntajes = [comparar(mi_vector, EMBEDDINGS[otra]) for otra in frase]
    porcentajes = repartir_atencion(puntajes)

    # nuevo vector = mezcla de TODOS los vectores, segun los porcentajes
    nuevo = [0.0] * len(mi_vector)
    for porcentaje, otra in zip(porcentajes, frase):
        for d in range(len(nuevo)):
            nuevo[d] += porcentaje * EMBEDDINGS[otra][d]
    return porcentajes, nuevo


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    frase = ["el", "gato", "come", "pescado"]
    print("Frase:", " ".join(frase))

    # 1) La tabla de atencion completa: cada fila es una palabra
    #    repartiendo su atencion entre toda la frase (cada fila suma 1)
    print("\nTabla de atencion (fila = quien mira, columna = a quien):\n")
    print(" " * 10 + "".join(f"{p:>10s}" for p in frase))
    for palabra in frase:
        porcentajes, _ = atender(palabra, frase)
        fila = "".join(f"{p:10.2f}" for p in porcentajes)
        print(f"{palabra:>10s}{fila}")

    # 2) Zoom a una palabra: como cambia el vector de "come"
    porcentajes, nuevo = atender("come", frase)
    print("\nVector original de 'come':   ", EMBEDDINGS["come"])
    print("Vector de 'come' tras atender:", [round(x, 2) for x in nuevo])
    print("""
Fijate: el nuevo vector de 'come' ya no es solo 'accion': ahora
lleva un poco de 'animal' (por gato) y de 'comida' (por pescado).
La palabra ABSORBIO su contexto. Eso es atencion.
""")

    # Nota: en un Transformer real estos vectores no se escriben a
    # mano: la red los aprende sola durante el entrenamiento, y la
    # atencion se calcula con matrices entrenables. Pero los 3 pasos
    # son exactamente estos: comparar, repartir, mezclar.
