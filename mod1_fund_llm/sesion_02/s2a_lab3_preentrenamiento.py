"""

Fase 3: PRE-ENTRENAMIENTO - nace un modelo BASE
======================================================
¿Como se entrena un LLM? En dos (o tres) etapas. La primera es el
PRE-ENTRENAMIENTO: mostrarle muchisimo texto crudo para que aprenda
a predecir el token siguiente. El resultado se llama MODELO BASE.

Para verlo no necesitamos redes neuronales: usamos el modelo de
CONTAR de la sesion 1 (entrenar = contar que viene despues de que),
solo que ahora cuenta PALABRAS con 4 de contexto en vez de letras.

Lo importante de este lab es la leccion final:

    El modelo base sabe CONTINUAR texto como el que leyo...
    pero NO sabe conversar. Ante una pregunta se queda mudo,
    porque en su corpus nunca vio una pregunta.

Cada funcion es un bloque conceptual (todas de la sesion 1):

    tokenizar()  -> partir el texto en palabras       (lab 4)
    entrenar()   -> contar                            (labs 1 y 3)
    predecir()   -> elegir al azar segun frecuencias  (lab 1)
    generar()    -> predecir, pegar y repetir         (lab 1)
"""

import random
import re

CONTEXTO = 6   # cuantas palabras atras mira


def tokenizar(texto):
    """Partir el texto en palabras y signos (lab 4 de la sesion 1)."""
    return re.findall(r"\w+|[^\w\s]", texto, re.UNICODE)


def entrenar(tokens, modelo=None):
    """ENTRENAR = contar. Para cada grupo de CONTEXTO palabras,
    anotar que palabra vino despues. El diccionario ES el modelo.

    Detalle nuevo: si recibe un modelo ya entrenado, SIGUE contando
    sobre el (esa puertita sera el fine-tuning del lab 4)."""
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
    """PREDECIR = elegir al azar segun las frecuencias vistas.
    Devuelve None si NUNCA vio ese contexto (el modelo 'se queda
    mudo': no tiene ni idea de como seguir)."""
    if clave not in modelo:
        return None
    return random.choice(modelo[clave])


def generar(modelo, tokens_semilla, cantidad):
    """GENERAR = predecir, pegar y repetir (lab 1 de la sesion 1)."""
    tokens = list(tokens_semilla)
    for _ in range(cantidad):
        clave = tuple(tokens[-CONTEXTO:])
        siguiente = predecir(modelo, clave)
        if siguiente is None:
            tokens.append("[No tengo información en mi contexto sobre esta consulta]")
            break
        tokens.append(siguiente)
    texto = " ".join(tokens)
    return re.sub(r" ([^\w\s])", r"\1", texto)   # pegar la puntuacion


# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # 1) El corpus de pre-entrenamiento: texto crudo, sin formato de
    #    pregunta/respuesta (pasaje de "Tradiciones Peruanas" de
    #    Ricardo Palma; dominio publico, Project Gutenberg 21282)
    #texto = open("mod1_fund_llm/sesion_01/data/mi_texto.txt", encoding="utf-8").read().lower()
    texto = open("mi_texto.txt", encoding="utf-8").read().lower()
    texto = " ".join(texto.split())
    tokens = tokenizar(texto)

    # 2) PRE-ENTRENAR = contar todo el corpus
    modelo = entrenar(tokens)
    print(f"corpus: {len(tokens)} palabras | contextos aprendidos: {len(modelo)}")

    # 3) El modelo base CONTINUA texto igualito a su corpus...
    print("\n--- El modelo base continuando texto ---")
    print(generar(modelo, tokens[:CONTEXTO], cantidad=40))

    # 4) ...pero ante una pregunta SE QUEDA MUDO
    pregunta = tokenizar("pregunta: donde esta la casa del almirante? respuesta:")
    print("\n--- El mismo modelo ante una pregunta ---")
    print(generar(modelo, pregunta, cantidad=20))

    # Nota 1: aqui "contar" tarda nada. Pre-entrenar un LLM real es
    # la etapa carisima: billones de palabras, meses de computo,
    # millones de dolares. Por eso se hace UNA vez y el resultado
    # (el modelo base) se guarda y se reutiliza.
    #
    # Nota 2: el modelo base no es tonto: es un experto en continuar
    # texto. Su problema es que nadie le enseño el FORMATO de una
    # conversacion. Enseñarselo es el fine-tuning: lab 4.
