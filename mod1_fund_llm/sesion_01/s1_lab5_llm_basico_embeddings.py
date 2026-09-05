"""
Fase 4: EMBEDDINGS
======================================================
Ya sabemos convertir texto en tokens (numeros), pero esos numeros
no dicen nada sobre el SIGNIFICADO de la palabra. El numero 7 no es
"mas parecido" al 8 solo porque este al lado.

Un EMBEDDING es otra cosa: representar cada palabra como una LISTA
de numeros (un "vector"), elegida de forma que palabras con
significados o usos parecidos queden con vectores parecidos.

Aqui no vamos a entrenar una red neuronal (eso lo hacen los LLMs reales),
pero SI vamos a construir embeddings simples usando una idea real:

    "Una palabra se parece a las palabras con las que suele aparecer."
    (esto se llama la Hipotesis Distribucional)

Cada funcion es un bloque conceptual:

    tokenizar()            -> reusamos la idea del lab de tokenizacion
    construir_vocabulario() -> igual que antes
    construir_embeddings()  -> cuenta con que palabras aparece cada palabra
    similitud_coseno()      -> mide que tan parecidos son dos vectores
    palabras_mas_parecidas() -> encuentra los vecinos de una palabra
 
"""

import re
import math


def tokenizar(texto):
    return re.findall(r"\w+|[^\w\s]", texto, re.UNICODE)


def construir_vocabulario(tokens):
    vocab = {}
    for token in tokens:
        if token not in vocab:
            vocab[token] = len(vocab)
    return vocab


def construir_embeddings(tokens, vocab, ventana=2):
    """
    CONSTRUIR EMBEDDINGS = para cada palabra, crear un vector donde
    cada posicion cuenta cuantas veces aparecio OTRA palabra cerca
    de ella (dentro de la "ventana" de contexto).

    Si "hola" y "chau" siempre aparecen cerca de "mundo" y "amigo",
    sus vectores terminaran pareciendose, aunque nunca las hayamos
    comparado directamente. Asi "aprenden" significado por contexto.
    """
    tamano_vocab = len(vocab)
    # cada palabra empieza con un vector de puros ceros
    embeddings = {palabra: [0] * tamano_vocab for palabra in vocab}

    for i, palabra in enumerate(tokens):
        inicio = max(0, i - ventana)
        fin = min(len(tokens), i + ventana + 1)
        for j in range(inicio, fin):
            if j == i:
                continue
            vecino = tokens[j]
            indice_vecino = vocab[vecino]
            embeddings[palabra][indice_vecino] += 1  # suma un "vecino visto"

    return embeddings


def similitud_coseno(v1, v2):
    """
    SIMILITUD COSENO = mide el angulo entre dos vectores.
    1.0  -> apuntan exactamente igual (muy parecidos)
    0.0  -> no tienen relacion
    Es la metrica que usan los LLMs reales para comparar embeddings.
    """
    producto_punto = sum(a * b for a, b in zip(v1, v2))
    norma1 = math.sqrt(sum(a * a for a in v1))
    norma2 = math.sqrt(sum(b * b for b in v2))
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return producto_punto / (norma1 * norma2)


def palabras_mas_parecidas(palabra, embeddings, top_n=3):
    """
    Compara el embedding de 'palabra' contra TODOS los demas
    y devuelve los mas parecidos, ordenados de mayor a menor.
    """
    if palabra not in embeddings:
        return []

    vector_objetivo = embeddings[palabra]
    similitudes = []
    for otra_palabra, vector in embeddings.items():
        if otra_palabra == palabra:
            continue
        score = similitud_coseno(vector_objetivo, vector)
        similitudes.append((otra_palabra, score))

    similitudes.sort(key=lambda par: par[1], reverse=True)
    return similitudes[:top_n]


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # Texto de ejemplo: "hola" y "chau" aparecen en contextos parecidos
    # a proposito, para que el embedding lo detecte.
    texto = """
    hola mundo. hola amigo. hola marta. chau mundo. chau amigo.
    chau marta. el gato come pescado. el perro come carne.
    el gato duerme mucho. el perro duerme mucho.
    """.lower()

    tokens = tokenizar(texto)
    vocab = construir_vocabulario(tokens)

    print(f"Vocabulario ({len(vocab)} palabras): {list(vocab.keys())}")

    # 1) Construir los embeddings por co-ocurrencia
    embeddings = construir_embeddings(tokens, vocab, ventana=2)

    for k, v in embeddings.items():
        print(f"{k}:{v}")


    print(f"\nEmbedding de 'hola' (vector de {len(embeddings['hola'])} numeros):")
    print(embeddings["hola"])

    # 2) Comparar dos palabras directamente
    sim = similitud_coseno(embeddings["hola"], embeddings["chau"])
    print(f"\nSimilitud entre 'hola' y 'chau': {sim:.2f}")

    sim2 = similitud_coseno(embeddings["hola"], embeddings["gato"])
    print(f"Similitud entre 'hola' y 'gato': {sim2:.2f}")

    # 3) Buscar las palabras mas parecidas a varias palabras
    for palabra in ["hola", "gato", "come"]:
        vecinas = palabras_mas_parecidas(palabra, embeddings, top_n=3)
        print(f"\nPalabras mas parecidas a '{palabra}':")
        for vecina, score in vecinas:
            print(f"   {vecina:10s} -> similitud {score:.2f}")

    # Nota: los LLMs reales no cuentan vecinos a mano como aca.
    # Entrenan estos vectores con redes neuronales sobre textos enormes,
    # y usan cientos o miles de numeros por palabra (no solo el tamaño
    # del vocabulario). Pero la idea de fondo es la misma que viste aqui:
    # palabras que aparecen en contextos parecidos, terminan con
    # vectores parecidos.
