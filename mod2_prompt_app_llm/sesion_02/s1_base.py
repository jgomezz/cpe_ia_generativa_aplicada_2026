
from langchain.chat_models import init_chat_model


# Funciones basicas

def get_modelo(prefix_model, temperature=0.8):
    """
    Obtiene el modelo
    """
    llm = init_chat_model(
                        model=prefix_model,
                        #temperature=temperature,
                        )
    return llm

