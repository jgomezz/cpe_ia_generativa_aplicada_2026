"""

Fase 5: RLHF - aprender de preferencias (version para contar)
======================================================
Tras el fine-tuning el modelo ya responde con el formato correcto,
pero le quedan vicios: sigue parloteando despues de responder, se
repite, corta a mitad de frase... Ya no hay "respuesta correcta"
que enseñarle; solo podemos decir CUAL respuesta PREFERIMOS.

Para eso existe la tercera etapa de crianza de un LLM:

    RLHF = Reinforcement Learning from Human Feedback
    (aprendizaje por refuerzo con retroalimentacion humana)

El ciclo, con nuestro modelo de contar:

    1) GENERAR  -> el modelo produce varias respuestas candidatas
                   (salen distintas: elegir al azar ya es variedad)
    2) PUNTUAR  -> una funcion de RECOMPENSA dice cuales preferimos
                   (una regla simple juega el papel del humano)
    3) REFORZAR -> volver a CONTAR las respuestas premiadas, como
                   si el modelo las hubiera leido otra vez: ahora
                   son mas probables
    4) repetir

Mira la "recompensa media" ronda a ronda: sube.

Usamos CONTEXTO = 2 (no 4): con menos contexto el modelo duda mas
y sus respuestas varian mas. Para explorar hay que arriesgar: un
modelo que siempre dice lo mismo no tiene de donde aprender.
"""

import random
import re

CONTEXTO = 2   # menos contexto = mas variedad para explorar


def tokenizar(texto):
    return re.findall(r"\w+|[^\w\s]", texto, re.UNICODE)


def entrenar(tokens, modelo=None):
    """ENTRENAR = contar (y REFORZAR = contar otra vez lo premiado)."""
    if modelo is None:
        modelo = {}
    for i in range(len(tokens) - CONTEXTO):
        clave = tuple(tokens[i:i + CONTEXTO])
        siguiente = tokens[i + CONTEXTO]
        if clave not in modelo:
            modelo[clave] = []
        modelo[clave].append(siguiente)
    return modelo


def continuar(modelo, tokens_prompt, cantidad):
    """Generar una respuesta y devolver SOLO los tokens nuevos."""
    tokens = list(tokens_prompt)
    for _ in range(cantidad):
        clave = tuple(tokens[-CONTEXTO:])
        if clave not in modelo:
            break
        tokens.append(random.choice(modelo[clave]))
    return tokens[len(tokens_prompt):]


def recompensa(tokens_respuesta):
    """El 'humano' del experimento, reducido a tres gustos:
        +1.0 si cierra la frase pronto (un '.' en los primeros 10)
        -1.0 si sigue parloteando (se inventa otra 'pregunta')
        -1.0 por cada palabra repetida dos veces seguidas
    En el RLHF real esta funcion es un MODELO DE RECOMPENSA:
    una red entrenada con miles de comparaciones humanas
    ("¿cual de estas dos respuestas prefieres?")."""
    puntos = 0.0
    if "." in tokens_respuesta[:10]:
        puntos += 1.0
    if "pregunta" in tokens_respuesta:
        puntos -= 1.0
    for a, b in zip(tokens_respuesta, tokens_respuesta[1:]):
        if a == b:
            puntos -= 1.0
    return puntos


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    random.seed(0)   # para que la corrida sea repetible

    # 1) Modelo base + fine-tuning (labs 3 y 4, en tres lineas)
    corpus = open("mod1_fund_llm/sesion_01/data/mi_texto.txt", encoding="utf-8").read().lower()
    dialogos = open("mod1_fund_llm/sesion_02/data/dialogos.txt", encoding="utf-8").read().lower()
    modelo = entrenar(tokenizar(" ".join(corpus.split())))
    modelo = entrenar(tokenizar(" ".join(dialogos.split())), modelo=modelo)

    preguntas = [
        "donde esta la casa del almirante?",
        "como era el tal almirante?",
        "quien fabrico la soberbia casa?",
        "que fuente de autoridad tiene esta tradicion?",
    ]
    prompts = [tokenizar(f"pregunta: {p} respuesta:") for p in preguntas]

    CANDIDATAS = 10   # respuestas que genera por pregunta
    LARGO = 14        # tokens por respuesta

    # 2) El ciclo del RLHF
    for ronda in range(6):
        premiadas = []
        total = 0.0
        cuenta = 0

        for prompt in prompts:
            for _ in range(CANDIDATAS):
                respuesta = continuar(modelo, prompt, LARGO)
                puntos = recompensa(respuesta)
                total += puntos
                cuenta += 1
                if puntos >= 1.0:
                    # premiada: cierra pronto, sin parlotear ni repetirse
                    premiadas.append(prompt + respuesta)

        print(f"ronda {ronda} | recompensa media: {total / cuenta:+.2f} "
              f"| premiadas: {len(premiadas)}")

        # 3) REFORZAR: contar las premiadas otra vez (dos veces,
        #    para que pesen). Lo preferido se vuelve mas probable.
        for premiada in premiadas:
            modelo = entrenar(premiada, modelo=modelo)
            modelo = entrenar(premiada, modelo=modelo)

    # 4) Resultado: las mismas preguntas con el modelo reforzado
    print("\n--- Respuestas despues del RLHF ---")
    for pregunta, prompt in zip(preguntas[:3], prompts[:3]):
        respuesta = " ".join(continuar(modelo, prompt, 12))
        respuesta = re.sub(r" ([^\w\s])", r"\1", respuesta)
        print(f"{pregunta} -> {respuesta}")

    # Dos notas honestas:
    # 1) El RLHF real no "cuenta dos veces": usa un modelo de
    #    recompensa y algoritmos de refuerzo (PPO y familia) para
    #    ajustar la red neuronal. Pero el ciclo es este mismo:
    #    generar -> puntuar -> reforzar lo preferido.
    # 2) Cuidado con el REWARD HACKING: si la recompensa solo
    #    premiara "un punto pronto", al modelo le convendria
    #    responder '.' y nada mas. Los modelos encuentran los
    #    huecos de la regla que escribas; diseñar recompensas
    #    es la parte dificil del RLHF.
