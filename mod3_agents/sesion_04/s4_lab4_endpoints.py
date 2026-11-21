"""
Primera Aplicación con FastAPI

Probar con el navegador web :

    http://localhost:8040/docs


"""

from anyio import Path
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, Header
import uvicorn

from pydantic import BaseModel, Field
from s4_lab4_datos import PEDIDOS
from s4_lab4_agente import crear_agente

import os
from dotenv import load_dotenv

# ==========================
# 1. CONFIGURACION
# ==========================
app = FastAPI(title="Introducción a Pydantic")
agent = crear_agente()

load_dotenv()
AGENTE_API_KEY = os.getenv("AGENTE_API_KEY")  # Asegúrate de tener

# ==========================
# 2. REGLAS DE ENTRADA Y SALIDA
# ==========================

class ConsultaPedido(BaseModel):
    numero: str = Field(min_length=5, max_length=5, description="Número de pedido de 5 dígitos")

class PedidoRespuesta(BaseModel):
    numero: str
    estado: str

class Pregunta(BaseModel):
    mensaje: str

class Respuesta(BaseModel):
    respuesta: str


# ==========================
#  2. API REST
# ==========================
@app.get("/pedidos/{numero}", response_model=PedidoRespuesta)
def obtener_pedido(numero: str):
    """
        Obtiene el estado de un pedido a partir de su número.
    """
    if numero not in PEDIDOS:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return PedidoRespuesta(numero=numero, estado=PEDIDOS[numero])


@app.post("/pedidos/consulta", response_model=PedidoRespuesta)
def consultar_pedido(consulta: ConsultaPedido):
    """
        Consulta el estado de un pedido a partir de su número.
    """
    return obtener_pedido(consulta.numero)


@app.post("/chat", response_model=Respuesta)
async def chat(pregunta: Pregunta, x_api_key: str = Header(default="")):
    """
        Envía una pregunta al agente y recibe una respuesta.
    """
    #if x_api_key != AGENTE_API_KEY:
    #    raise HTTPException(status_code=401, detail="Clave API inválida")

    try:
        resultado = await agent.ainvoke({"messages":[{"role": "user", "content": pregunta.mensaje}]})
    except Exception as e:
        print(f"Error al interactuar con el agente: {e}") 
        raise HTTPException(status_code=500, detail="Error al interactuar con el agente")

    return Respuesta(respuesta=resultado["messages"][-1].text)

@app.get("/")
def pagina_chat():
    """Entrega la página web del chat."""
    return FileResponse(Path(__file__).parent / "s4_lab4_cliente.html")

# ==========================
#  3. EJECUCION
# ==========================
if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8040)

