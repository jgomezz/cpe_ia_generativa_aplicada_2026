"""
Fase 3: TOKENIZACION
======================================================
Antes de que un LLM pueda "pensar" en un texto, necesita
convertirlo en piezas mas pequeñas llamadas TOKENS.

Un token puede ser:
    - una letra        ("h", "o", "l", "a")
    - una palabra       ("hola", "mundo")
    - un pedazo de palabra ("hol", "a")  <- asi funcionan los LLMs reales

Cada funcion es un bloque conceptual de la tokenizacion:

    tokenizar_por_caracteres()  -> parte el texto letra por letra
    tokenizar_por_palabras()    -> parte el texto palabra por palabra
    construir_vocabulario()     -> junta todos los tokens unicos y les da un numero
    codificar()                 -> convierte tokens en numeros (lo que entiende el modelo)
    decodificar()                -> convierte numeros de vuelta en tokens (lo que entendemos nosotros)

"""

import re


def tokenizar_por_caracteres(texto):
    """
    La forma mas simple de tokenizar: cada letra es un token.
    Es lo que usamos en los labs 1, 2 y 3 sin darnos cuenta.
    """
    return list(texto)


def tokenizar_por_palabras(texto):
    """
    Parte el texto en palabras, separando tambien la puntuacion
    para que "mundo." no sea un token distinto de "mundo".
    """
    return re.findall(r"\w+|[^\w\s]", texto, re.UNICODE)


def construir_vocabulario(tokens):
    """
    VOCABULARIO = la lista de todos los tokens distintos que existen,
    cada uno con un numero (id) asignado.
    Un LLM no entiende texto, solo entiende estos numeros.
    """
    vocab = {}
    for token in tokens:
        if token not in vocab:
            vocab[token] = len(vocab)  # el siguiente numero disponible
    return vocab


def codificar(tokens, vocab):
    """
    CODIFICAR = cambiar cada token por su numero en el vocabulario.
    Esto es lo que realmente "ve" el modelo cuando le mandas texto.
    """
    return [vocab[token] for token in tokens]


def decodificar(ids, vocab):
    """
    DECODIFICAR = el camino inverso: de numeros a texto,
    para que un humano pueda leer lo que respondio el modelo.
    """
    vocab_inverso = {numero: token for token, numero in vocab.items()}
    return [vocab_inverso[i] for i in ids]


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":

    
    texto = "Hola mundo, hola Marta, hola Mateo. Hola mundo cruel, Hola Jaime!".lower()
    

    # 1) Tokenizar de dos formas distintas
    tokens_char = tokenizar_por_caracteres(texto)

    print("Texto original:", texto)

    print(f"\nTokens por CARACTER ({len(tokens_char)} tokens):")
    print(tokens_char)


    tokens_pal = tokenizar_por_palabras(texto)

    print("Texto original:", texto)

    print(f"\nTokens por PALABRA ({len(tokens_pal)} tokens):")
    print(tokens_pal)

    # 2) Construir vocabulario de cada tipo
    vocab_char = construir_vocabulario(tokens_char)
    vocab_pal = construir_vocabulario(tokens_pal)

    print(f"\nTamaño del vocabulario por caracter: {len(vocab_char)}")
    print(f"Tamaño del vocabulario por palabra:  {len(vocab_pal)}")
    print("\nVocabulario por palabra:", vocab_pal)

    # 3) Codificar y decodificar una frase con el vocabulario de palabras
    frase = tokenizar_por_palabras("hola mundo mateo") # Estoy usando palabras del vocabulario de palabras, no de caracteres
    ids = codificar(frase, vocab_pal)
    texto_recuperado = decodificar(ids, vocab_pal)

    print("\nFrase:", frase)
    print("Codificada (numeros que ve el modelo):", ids)
    print("Decodificada de vuelta:", texto_recuperado)

    # Nota: los LLMs reales (GPT, Claude, etc.) no tokenizan por letra
    # ni por palabra completa, sino por "sub-palabras" (ej: "token", "izar").
    # Asi logran un vocabulario manejable sin perderse palabras nuevas o raras.
