"""
Primera Aplicación con FastAPI

Probar con el navegador web :

    http://localhost:8040/docs


"""

from fastapi import FastAPI, HTTPException
import uvicorn

from pydantic import BaseModel, Field
from s4_lab4_datos import PEDIDOS


# ==========================
# 1. CONFIGURACION
# ==========================
app = FastAPI(title="Introducción a Pydantic")

# ==========================
# 2. REGLAS DE ENTRADA Y SALIDA
# ==========================

class ConsultaPedido(BaseModel):
    numero: str = Field(min_length=5, max_length=5, description="Número de pedido de 5 dígitos")

class PedidoRespuesta(BaseModel):
    numero: str
    estado: str


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


# ==========================
#  3. EJECUCION
# ==========================
if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8040)

