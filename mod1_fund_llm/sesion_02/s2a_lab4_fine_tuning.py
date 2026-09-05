"""
Fase 4: FINE-TUNING - del modelo base al modelo que responde
======================================================
El modelo base del lab 3 se queda mudo ante una pregunta: en su
corpus nunca vio el formato "pregunta: ... respuesta: ...".

FINE-TUNING = tomar el modelo YA pre-entrenado y seguir
entrenandolo con POCOS ejemplos del comportamiento que queremos.
Con nuestro modelo de contar es literal:

    pre-entrenar = contar un corpus grande
    fine-tuning  = SEGUIR contando unos pocos dialogos de ejemplo

Fijate en la proporcion, que es la real:

    corpus de pre-entrenamiento: todo el texto (los cimientos)
    datos de fine-tuning:        12 dialogos    (el acabado)

El fine-tuning no le enseña el idioma (eso ya lo tiene): le
enseña el FORMATO de conversar. Por eso con tan poquito alcanza.

Las funciones son LAS MISMAS del lab 3 (estan copiadas aqui para
que el archivo corra solo). El unico paso nuevo esta marcado.
"""

import random
import re

CONTEXTO = 6   # cuantas palabras atras mira


def tokenizar(texto):
    return re.findall(r"\w+|[^\w\s]", texto, re.UNICODE)


def entrenar(tokens, modelo=None):
    """ENTRENAR = contar. Si recibe un modelo, sigue contando sobre el."""
    if modelo is None:
        modelo = {}
    for i in range(len(tokens) - CONTEXTO):
        clave = tuple(tokens[i:i + CONTEXTO])
        siguiente = tokens[i + CONTEXTO]
        if clave not in modelo:
            modelo[clave] = []
        modelo[clave].append(siguiente)
    return modelo


def predecir(modelo, clave):
    if clave not in modelo:
        return None
    return random.choice(modelo[clave])


def generar(modelo, tokens_semilla, cantidad):
    tokens = list(tokens_semilla)
    for _ in range(cantidad):
        siguiente = predecir(modelo, tuple(tokens[-CONTEXTO:]))
        if siguiente is None:
            tokens.append("[me quede mudo]")
            break
        tokens.append(siguiente)
    return re.sub(r" ([^\w\s])", r"\1", " ".join(tokens))


def preguntar(modelo, texto_pregunta):
    """Armar el prompt con el formato de los dialogos y generar."""
    prompt = tokenizar(f"pregunta: {texto_pregunta} respuesta:")
    return generar(modelo, prompt, cantidad=15)


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # 1) PRE-ENTRENAR el modelo base (igual que el lab 3)
    texto = open("mod1_fund_llm/sesion_01/data/mi_texto.txt", encoding="utf-8").read().lower()
    tokens_corpus = tokenizar(" ".join(texto.split()))
    modelo = entrenar(tokens_corpus)

    # 2) ANTES del fine-tuning: mudo ante las preguntas
    print("--- ANTES del fine-tuning (modelo base) ---")
    print(preguntar(modelo, "donde esta la casa del almirante?"))
    print(preguntar(modelo, "como era el tal almirante?"))

    # 3) FINE-TUNING: seguir contando sobre EL MISMO modelo,
    #    ahora con los 12 dialogos de ejemplo  <- EL PASO NUEVO
    dialogos = open("mod1_fund_llm/sesion_02/data/dialogos.txt", encoding="utf-8").read().lower()
    tokens_dialogos = tokenizar(" ".join(dialogos.split()))
    print(f"\ndatos de ajuste: {len(tokens_dialogos)} palabras de dialogos\n")

    modelo = entrenar(tokens_dialogos, modelo=modelo)

    # 4) DESPUES: las mismas preguntas
    print("--- DESPUES del fine-tuning ---")
    print("\n" + preguntar(modelo, "donde esta la casa del almirante?"))
    print("\n" + preguntar(modelo, "como era el tal almirante?"))
    print("\n" + preguntar(modelo, "quien fabrico la soberbia casa?"))

    # Nota 1: responde bien porque las 6 palabras finales de cada
    # pregunta (p.ej. "casa del almirante ? respuesta :") apuntan a
    # SU respuesta. Prueba bajar CONTEXTO a 4 o a 2 y veras al modelo
    # mezclar respuestas de preguntas distintas: con "almirante ?
    # respuesta :" terminan DOS preguntas diferentes, y el modelo ya
    # no sabe cual le preguntaron. Menos contexto = mas confusion
    # (por eso los LLM reales pelean por contextos cada vez mas largos).
    #
    # Nota 2: en un LLM real el fine-tuning no es "contar mas":
    # es seguir entrenando la red neuronal (con millones de
    # conversaciones de ejemplo escritas por humanos). Asi se
    # convirtio GPT-3 (base) en ChatGPT. Pero la idea es esta:
    # poquitos datos buenos, sobre un modelo que ya sabe mucho.
    #
    # Nota 3: ¿y si responde con el formato correcto pero sigue
    # parloteando o inventando? Para pulir PREFERENCIAS (no
    # formatos) hay una tercera etapa: el RLHF del lab 5.
