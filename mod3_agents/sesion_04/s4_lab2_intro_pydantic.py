"""
Primera Aplicación con FastAPI

Probar con el navegador web :

    http://localhost:8040/docs


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

# ==========================
#  3. EJECUCION
# ==========================
if __name__ == "__main__":


    uvicorn.run(app, host="127.0.0.1", port=8040)

    '''
    # Para reconocer en calientes los cambios en el codigo 
    # El primer argumento debe incluir el nombre del archivo y el objeto app, separados por dos puntos
    # El parámetro reload=True permite que el servidor se reinicie automáticamente al detectar cambios en el código
    uvicorn.run("s4_lab2_intro_pydantic:app", host="127.0.0.1", port=8040, reload=True)
    '''

