from dotenv import load_dotenv
import os
import logging
from s1_base import get_modelo
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

load_dotenv()

prefix_model = os.getenv("PREFIX_MODEL")

llm = get_modelo(prefix_model)

from langchain_core.messages import SystemMessage, HumanMessage

msgs =  [
            SystemMessage(content="Eres un asistente experto en inteligencia artificial. Responde con un minimo de 500 palabras."),
            HumanMessage(content="Que es un agente de inteligencia artificial?")
        ]

for chunk in llm.stream(msgs):
    print(chunk.text, end="", flush=True)
print()


