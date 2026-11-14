import sys
from pathlib import Path
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

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
load_dotenv(override = True)

prefix_model = os.getenv("PREFIX_MODEL")

# Obtención del modelo
llm = get_llm(prefix_model)



CONEXIONES = {
    "tiendaya": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable-http",
    },
    "discord": {
        "url": "http://localhost:8002/mcp",
        "transport": "streamable-http",
    }
}


async def main():

    cliente = MultiServerMCPClient(CONEXIONES)
    #herramientas = await cliente.get_tools()
    herramientas = await cliente.get_tools(server_name="discord")          # se vuelven a descubrir

    for h in herramientas:
        print(f"{h.name}: {h.description}")

    from langchain.agents import create_agent

    agente = create_agent(
        model=llm,
        tools=herramientas,                      # herramientas del servidor MCP
        system_prompt=(
            "Eres el agente de NOTIFICACIONES de TiendaYa. Publicas en Discord el aviso que recibes, "
            "en un solo mensaje breve. Usa solo los datos recibidos; no agregues otros. "
            "Luego informa si el mensaje se publicó."
        ),
    )

    r = await agente.ainvoke({"messages": [("user", "Hola, por favor envía un mensaje a Discord con el texto: '¡Hola de nuevo desde TiendaYa!'")]})
    print(r)


if __name__ == "__main__":
    asyncio.run(main())