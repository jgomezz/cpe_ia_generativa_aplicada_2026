import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

import logging


# Generar una funcion que obtenga el modelo LLM

def get_llm(prefix_model, temperature=0.9):
    """
    Obtiene un modelo de lenguaje (LLM) basado en el modelo especificado.

    Args:
        model (str): El nombre del modelo a utilizar.
        temperature (float, optional): La temperatura para la generación de texto. 
                                        Valores más altos producen respuestas más creativas.
                                        Valores más bajos producen respuestas más deterministas.
                                        Por defecto es 0.9.

    Returns:
        llm: Un objeto de modelo de lenguaje inicializado.
    """
    llm = init_chat_model(
                            model=prefix_model, 
                            # temperature=temperature
                          )
    return llm


# Configuración del modelo de lenguaje
load_dotenv()

prefix_model = os.getenv("PREFIX_MODEL")

# Obtención del modelo
llm = get_llm(prefix_model)