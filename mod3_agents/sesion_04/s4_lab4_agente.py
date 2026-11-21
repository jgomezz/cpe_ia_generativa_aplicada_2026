'''
    Agente de pedidos de la tienda.
    Proporciona información sobre el estado de los pedidos y las políticas de la tienda.
'''

import os
import logging
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from s4_lab4_datos import PEDIDOS, POLITICAS


logging.getLogger("google_genai.models").setLevel(logging.ERROR)
load_dotenv()

SYSTEM_PROMPT = """ 
                Eres el asistente de TiendaYa. Usa las herramientas para obtener los datos; 
                no los inventes. Responde de forma breve y cordial.
            """

def get_llm(prefix_model):
    """Obtiene el modelo de lenguaje indicado en PREFIX_MODEL."""
    return init_chat_model(model=prefix_model)


@tool
def consultar_pedido(numero_pedido: str) -> str:
    """
        Consulta el estado de un pedido de TiendaYa.
    """
    return PEDIDOS.get(numero_pedido, "No existe ese pedido.")


@tool
def consultar_politica(tema: str) -> str:
    """
        Devuelve la política de TiendaYa sobre 'devoluciones' o 'envios'.
    """
    return POLITICAS.get(tema.lower(), "No existe esa política.")

# Obtengo el modelo LLM
llm = get_llm(os.getenv("PREFIX_MODEL"))  # 

# Creo el agente
def crear_agente(checkpointer=None):
    """
        Crea el agente de TiendaYa. Con un checkpointer, el agente tiene memoria.
    """
    return create_agent(
        model=llm,
        tools=[consultar_pedido, consultar_politica],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

