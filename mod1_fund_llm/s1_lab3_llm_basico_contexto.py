"""
Fase 2: LLM simple CON CONTEXTO
================================
En la version 2 el modelo miraba solo 1 letra atras.
Ahora mira las ultimas N letras (el "contexto").
 
Cambia CONTEXTO = 1, 2, 3, 4 y compara los resultados.
Descubriras que mas contexto = texto mas coherente...
hasta cierto punto (¡ejecutalo y ve que pasa con 6 u 8!).
 
"""

import random


def entrenar(texto, contexto):
    """
    ENTRENAR = contar, igual que antes, pero ahora la clave
    del diccionario no es 1 letra sino las ultimas N letras.
    Ejemplo con contexto=2:
        despues de "qu" vio ['e', 'i', 'e', 'e', ...]
    """
    modelo = {}
    for i in range(len(texto) - contexto):
        clave = texto[i:i + contexto]          # las N letras anteriores
        siguiente = texto[i + contexto]        # la letra que vino despues
        if clave not in modelo:
            modelo[clave] = []
        modelo[clave].append(siguiente)
    return modelo


def predecir(modelo, letra):
    """
    PREDECIR = igual que antes: elegir al azar segun
    las frecuencias vistas para ese contexto.
    """
    if letra not in modelo:
        return None
    return random.choice(modelo[letra])


def generar(modelo, semilla, cantidad, contexto):
    """
    GENERAR = predecir, pegar y repetir.
    La diferencia clave: para predecir cada letra,
    usamos las ULTIMAS N letras de lo ya escrito.
    El modelo "recuerda" lo que acaba de decir.
    """
    resultado = semilla
    for _ in range(cantidad):
        clave = resultado[-contexto:]      # mirar las ultimas N letras
        letra = predecir(modelo, clave)
        if letra is None:
            break
        resultado += letra
    return resultado

# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # 1) Datos: pasaje de "Tradiciones Peruanas" de Ricardo Palma
    #    (dominio publico; fuente: Project Gutenberg, ebook 21282).
    texto = open("mi_texto.txt", encoding="utf-8").read().lower()
    
    texto = " ".join(texto.split())   # limpiar saltos de linea y espacios extra



    # 3) Probar con distintos tamaños de contexto
    for contexto in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        modelo = entrenar(texto, contexto)

        # for key, value in modelo.items():
        #    print(f"Despues de '{key}' vio: {value}")

        semilla = texto[:contexto]           # empezar con el inicio del texto
        salida = generar(modelo, semilla, cantidad=150, contexto=contexto)
        print(f"\n--- Semilla = '{semilla}' | Contexto = {contexto} letra(s) ---")
        print(salida)