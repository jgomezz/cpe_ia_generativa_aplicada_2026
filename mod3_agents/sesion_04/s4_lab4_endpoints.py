"""
Primera Aplicación con FastAPI

Probar con el navegador web :

    http://localhost:8040/docs


"""

from fastapi import FastAPI, HTTPException
import uvicorn

from pydantic import BaseModel, Field
from s4_lab4_datos import PEDIDOS
from s4_lab4_agente import crear_agente

# ==========================
# 1. CONFIGURACION
# ==========================
app = FastAPI(title="Introducción a Pydantic")
agent = crear_agente()

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
async def chat(pregunta: Pregunta):
    """
        Envía una pregunta al agente y recibe una respuesta.
    """
    try:
        resultado = await agent.ainvoke({"messages":[{"role": "user", "content": pregunta.mensaje}]})
    except Exception as e:
        print(f"Error al interactuar con el agente: {e}") 
        raise HTTPException(status_code=500, detail="Error al interactuar con el agente")

    return Respuesta(respuesta=resultado["messages"][-1].text)


# ==========================
#  3. EJECUCION
# ==========================
if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8040)

