"""
Primera Aplicación con FastAPI

Probar con el navegador web :

    http://localhost:8040/docs

Ejecutar en consola:

    uvicorn mod3_agents.sesion_04.s4_lab3_uvicorn_run_consola:app --reload --port 8040
    

"""

from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel, Field

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
@app.post("/pedidos/consulta", response_model=PedidoRespuesta)
def consultar_pedido(consulta: ConsultaPedido):
    # Simular una respuesta de pedido
    return PedidoRespuesta(numero=consulta.numero, estado="En proceso")  


