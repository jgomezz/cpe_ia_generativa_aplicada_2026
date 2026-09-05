"""
El LLM Basico es un modelo de lenguaje muy simple, que aprende a predecir la siguiente letra de un texto.
======================================================
Cada funcion es un bloque conceptual de todo LLM:

    entrenar()  -> aprende de un texto
    predecir()  -> adivina la siguiente letra
    generar()   -> encadena predicciones para escribir texto

"""

import random


def entrenar(texto):
    """
    ENTRENAR = contar.
    Recorre el texto y anota, para cada letra,
    que letras aparecieron justo despues.
    El diccionario resultante ES el modelo.
    """
    modelo = {}
    for i in range(len(texto) - 1):
        actual = texto[i]
        siguiente = texto[i + 1]
        if actual not in modelo:
            modelo[actual] = []
        modelo[actual].append(siguiente)
    return modelo


def predecir(modelo, letra):
    """
    PREDECIR = elegir la siguiente letra al azar,
    pero segun las frecuencias que vio el modelo.
    Si despues de 'l' vio ['a','a','a','a','i'],
    elegira 'a' el 80% de las veces.
    Devuelve None si nunca vio esa letra.
    """
    if letra not in modelo:
        return None
    return random.choice(modelo[letra])


def generar(modelo, semilla, cantidad):
    """
    GENERAR = predecir, pegar y repetir.
    Empieza con la semilla y encadena predicciones,
    una letra a la vez (igual que hace ChatGPT,
    pero con tokens en vez de letras).
    """
    letra = semilla
    resultado = semilla
    for _ in range(cantidad):
        letra = predecir(modelo, letra)
        if letra is None:
            break
        resultado += letra
    return resultado


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # 1) Datos de entrenamiento: inicio con datos publicos.
    #    Tambien puedes cargar cualquier archivo asi:
    texto = open("mi_texto.txt", encoding="utf-8").read().lower()

    # limpieza de datos
    texto = " ".join(texto.split())   # limpiar saltos de linea y espacios extra

    # 2) Entrenar el modelo
    modelo = entrenar(texto)

    for key, value in modelo.items():
        print(f"Despues de '{key}' puedes continuar con: {value}")

    #print("Despues de 'h' vio:", modelo["h"])
    #print("Despues de 'l' vio:", modelo["l"])

    # 3) Generar texto nuevo
    #salida = generar(modelo, semilla="h", cantidad=40)
    salida = generar(modelo, semilla="e", cantidad=100)

    print("\nTexto generado:", salida)