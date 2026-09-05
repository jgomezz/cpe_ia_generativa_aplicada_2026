"""
Fase 6: PARAMETROS - temperature, top_p, top_k
======================================================
Desde el lab 1 de la sesion 1, "predecir" termina igual: mirar las
frecuencias y elegir al azar. Ese "elegir al azar" tiene perillas,
y son las mismas que ves en la API de cualquier LLM:

    TEMPERATURE -> cuanta ventaja le das al favorito.
                   T baja = casi siempre gana el mas frecuente
                   (conservador). T alta = todos tienen chance
                   (arriesgado y creativo... o disparatado).
    TOP_K       -> solo los K mas frecuentes pueden salir.
                   El resto queda eliminado del sorteo.
    TOP_P       -> ordenar de mas a menos probable y quedarse con
                   los primeros que junten una probabilidad p.
                   El grupo se adapta solo: chico si hay un claro
                   favorito, grande si hay empate.

Ojo: ninguna perilla cambia el modelo (los conteos son los mismos).
Cambian como se ELIGE. Mismo cerebro, distinto caracter.

Usamos el modelo de contar con CONTEXTO = 1: tras cada palabra hay
muchas opciones, perfecto para ver el efecto de cada perilla.
"""

import random
import re

CONTEXTO = 1


def tokenizar(texto):
    return re.findall(r"\w+|[^\w\s]", texto, re.UNICODE)


def entrenar(tokens):
    modelo = {}
    for i in range(len(tokens) - CONTEXTO):
        clave = tuple(tokens[i:i + CONTEXTO])
        siguiente = tokens[i + CONTEXTO]
        if clave not in modelo:
            modelo[clave] = []
        modelo[clave].append(siguiente)
    return modelo


def contar_opciones(modelo, clave):
    """De la lista de vecinos vistos a una tabla {palabra: veces},
    ordenada de mas a menos frecuente."""
    conteos = {}
    for palabra in modelo.get(clave, []):
        conteos[palabra] = conteos.get(palabra, 0) + 1
    return dict(sorted(conteos.items(), key=lambda par: par[1], reverse=True))


def aplicar_temperatura(conteos, temperatura):
    """TEMPERATURE: elevar cada conteo a la potencia 1/T y repartir.
    T=1 deja las frecuencias como estan. T chica agranda la ventaja
    del favorito; T grande la reduce y empareja el sorteo."""
    pesos = {p: c ** (1.0 / temperatura) for p, c in conteos.items()}
    suma = sum(pesos.values())
    return {p: peso / suma for p, peso in pesos.items()}


def aplicar_top_k(probabilidades, k):
    """TOP_K: quedarse con las K mas probables y repartir de nuevo."""
    mejores = dict(list(probabilidades.items())[:k])
    suma = sum(mejores.values())
    return {p: v / suma for p, v in mejores.items()}


def aplicar_top_p(probabilidades, p_objetivo):
    """TOP_P: quedarse con las mas probables hasta JUNTAR p_objetivo."""
    elegidas = {}
    acumulado = 0.0
    for palabra, prob in probabilidades.items():
        elegidas[palabra] = prob
        acumulado += prob
        if acumulado >= p_objetivo:
            break
    suma = sum(elegidas.values())
    return {p: v / suma for p, v in elegidas.items()}


def elegir(probabilidades):
    """El sorteo final, respetando las probabilidades que quedaron."""
    return random.choices(list(probabilidades), weights=probabilidades.values())[0]


def generar(modelo, semilla, cantidad, temperatura=1.0, top_k=None, top_p=None):
    """El generar() de siempre, pero el sorteo pasa por las perillas:
    temperatura -> top_k -> top_p -> elegir."""
    tokens = [semilla]
    for _ in range(cantidad):
        conteos = contar_opciones(modelo, tuple(tokens[-CONTEXTO:]))
        if not conteos:
            break
        probabilidades = aplicar_temperatura(conteos, temperatura)
        if top_k is not None:
            probabilidades = aplicar_top_k(probabilidades, top_k)
        if top_p is not None:
            probabilidades = aplicar_top_p(probabilidades, top_p)
        tokens.append(elegir(probabilidades))
    return re.sub(r" ([^\w\s])", r"\1", " ".join(tokens))


def imprimir_tabla(titulo, probabilidades, limite=5):
    pares = list(probabilidades.items())[:limite]
    fila = "  ".join(f"{p}: {v:.2f}" for p, v in pares)
    extra = f"  (+{len(probabilidades) - limite} mas)" if len(probabilidades) > limite else ""
    print(f"  {titulo:<12s} {fila}{extra}")


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    texto = open("mod1_fund_llm/sesion_01/data/mi_texto.txt", encoding="utf-8").read().lower()
    modelo = entrenar(tokenizar(" ".join(texto.split())))

    # 1) Las opciones REALES del modelo despues de la palabra "de"
    conteos = contar_opciones(modelo, ("de",))
    print(f"despues de 'de' el modelo vio {sum(conteos.values())} continuaciones,")
    print(f"{len(conteos)} palabras distintas. Las mas frecuentes:")
    print("  ", {p: c for p, c in list(conteos.items())[:5]})

    # 2) TEMPERATURE reparte ese sorteo
    print("\n1) TEMPERATURE (probabilidades despues de 'de'):")
    for t in [0.5, 1.0, 2.0]:
        imprimir_tabla(f"T={t}", aplicar_temperatura(conteos, t))
    print("   T baja -> el favorito arrasa. T alta -> sorteo parejo.")

    probabilidades = aplicar_temperatura(conteos, 1.0)

    # 3) TOP_K y TOP_P recortan la lista de candidatos
    print("\n2) TOP_K = 3 (solo los 3 mas probables compiten):")
    imprimir_tabla("", aplicar_top_k(probabilidades, 3))

    print("\n3) TOP_P = 0.5 (los mejores hasta juntar el 50%):")
    imprimir_tabla("", aplicar_top_p(probabilidades, 0.5))

    # 4) El mismo modelo, distinto caracter
    print("\n--- Generando desde 'el' con cada perilla ---")
    random.seed(7)
    for nombre, opciones in [
        ("T=0.3 (conservador)", dict(temperatura=0.3)),
        ("T=1.0 (neutro)",      dict(temperatura=1.0)),
        ("T=2.0 (arriesgado)",  dict(temperatura=2.0)),
        ("top_k=2",             dict(top_k=2)),
        ("top_p=0.6",           dict(top_p=0.6)),
    ]:
        print(f"\n[{nombre}]")
        print(generar(modelo, "el", cantidad=25, **opciones))

    # Nota 1: ¿viste que con T=0.3 el texto entra en un BUCLE y
    # repite la misma frase? Les pasa tambien a los LLM reales:
    # temperatura muy baja = siempre la opcion mas probable =
    # riesgo de quedarse dando vueltas. Un poco de azar ayuda.
    #
    # Nota 2: por eso "temperature baja" da respuestas repetibles y
    # serias, y "temperature alta" sirve para lluvia de ideas
    # (aceptando disparates). En las APIs reales la receta tipica es
    # tocar UNA de las perillas, no todas a la vez. Y ahora ya lo
    # sabes: no son magia, son formas de recortar y repartir un sorteo.
