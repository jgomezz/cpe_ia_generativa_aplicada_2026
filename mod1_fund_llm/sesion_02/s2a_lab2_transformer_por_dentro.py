"""

https://claude.ai/code/artifact/118b2c13-814f-4445-9a5f-f865b565ad0c?via=auto_preview

Fase 2: EL TRANSFORMER POR DENTRO
======================================================
Un Transformer (la T de GPT) es, visto de lejos, esta tuberia:

    texto -> tokens -> vectores -> [ATENCION x varias capas] -> prediccion

    1) tokens    -> partir el texto en piezas       (sesion 1, lab 4)
    2) vectores  -> cada token entra como embedding (sesion 1, lab 5)
    3) atencion  -> cada palabra absorbe su contexto     (lab 1)
    4) capas     -> repetir la atencion varias veces
    5) al final  -> un puntaje por cada posible token siguiente

Este lab agrega DOS ideas que faltaban:

    LA REGLA DE NO ESPIAR (mascara causal): el modelo se entrena
    prediciendo el token siguiente, asi que cada palabra solo puede
    mirar HACIA ATRAS. Mirar adelante seria ver la respuesta.

    LAS CAPAS: la atencion no se hace una vez, se APILA. En cada
    capa las palabras vuelven a mezclarse, ya enriquecidas por la
    capa anterior. GPT apila decenas de estas capas.

Reusamos las funciones del lab 1 (mismo codigo, otra regla).
"""

import math

#                       animal  comida  accion  articulo
EMBEDDINGS = {
    "el":      [0.0,    0.0,    0.0,    1.0],
    "gato":    [1.0,    0.0,    0.2,    0.0],
    "come":    [0.3,    0.6,    1.0,    0.0],
    "pescado": [0.0,    1.0,    0.0,    0.0],
}


def comparar(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


def repartir_atencion(puntajes):
    mayor = max(puntajes)
    exps = [math.exp(p - mayor) for p in puntajes]
    suma = sum(exps)
    return [e / suma for e in exps]


def atender_sin_espiar(posicion, frase, vectores):
    """Igual que atender() del lab 1, con LA REGLA DE NO ESPIAR:
    la palabra en 'posicion' solo compara y mezcla con las palabras
    de las posiciones 0 hasta la suya. El futuro no existe."""
    visibles = frase[:posicion + 1]              # <- la mascara causal

    mi_vector = vectores[posicion]
    puntajes = [comparar(mi_vector, vectores[i]) for i in range(len(visibles))]
    porcentajes = repartir_atencion(puntajes)

    nuevo = [0.0] * len(mi_vector)
    for porcentaje, i in zip(porcentajes, range(len(visibles))):
        for d in range(len(nuevo)):
            nuevo[d] += porcentaje * vectores[i][d]
    return porcentajes, nuevo


def capa_de_atencion(frase, vectores):
    """UNA CAPA = todas las palabras atienden (sin espiar) a la vez,
    y todas salen con vector nuevo. Apilar capas = repetir esto."""
    porcentajes_de_todos = []
    vectores_nuevos = []
    for posicion in range(len(frase)):
        porcentajes, nuevo = atender_sin_espiar(posicion, frase, vectores)
        porcentajes_de_todos.append(porcentajes)
        vectores_nuevos.append(nuevo)
    return porcentajes_de_todos, vectores_nuevos


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    frase = ["el", "gato", "come", "pescado"]
    vectores = [list(EMBEDDINGS[p]) for p in frase]
    print("Frase:", " ".join(frase))

    # 1) La tabla de atencion CON la regla de no espiar:
    #    el triangulo de arriba queda vacio (el futuro esta tapado)
    porcentajes_de_todos, vectores_capa1 = capa_de_atencion(frase, vectores)

    print("\nTabla de atencion con mascara causal (-- = no puede mirar):\n")
    print(" " * 10 + "".join(f"{p:>10s}" for p in frase))
    for palabra, porcentajes in zip(frase, porcentajes_de_todos):
        celdas = [f"{p:10.2f}" for p in porcentajes]
        celdas += [f"{'--':>10s}"] * (len(frase) - len(porcentajes))
        print(f"{palabra:>10s}{''.join(celdas)}")

    print("""
Lee las filas: 'el' solo se ve a si mismo (es la primera palabra);
'pescado' puede mirar toda la frase porque es la ultima. Gracias a
esta regla el modelo puede entrenarse a predecir el siguiente token
sin hacer trampa.""")

    # 2) APILAR CAPAS: pasar la frase por la atencion varias veces.
    #    Miremos como el vector de 'come' se enriquece capa a capa.
    print("Vector de 'come' capa por capa:\n")
    print(f"   entrada: {[round(x, 2) for x in vectores[2]]}")
    for capa in range(1, 4):
        _, vectores = capa_de_atencion(frase, vectores)
        print(f"   capa {capa}:  {[round(x, 2) for x in vectores[2]]}")

    print("""
En cada capa 'come' vuelve a mezclarse con sus vecinas, que a su
vez ya venian mezcladas: la informacion viaja cada vez mas lejos.
GPT apila DECENAS de capas como esta (y entre capa y capa agrega
una mini-red que 'digiere' lo mezclado).

Con la arquitectura clara, las preguntas que siguen son de crianza:
¿como se entrena? (lab 3), ¿como se especializa? (labs 4 y 5) y
¿como se controla al generar? (lab 6).""")
