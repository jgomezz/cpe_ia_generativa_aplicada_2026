"""
Primera Aplicación con FastAPI

Probar con el navegador web :

    http://localhost:8040/
    http://localhost:8040/saludo/Ana
    http://localhost:8040/docs


"""

from fastapi import FastAPI
import uvicorn

# ==========================
# 1. CONFIGURACION
# ==========================
app = FastAPI(title="Introducción a FastAPI")

# ==========================
#  2. API REST
# ==========================
@app.get("/")
def inicio():
    return {"mensaje": "¡Bienvenido a la API de FastAPI!"}  

@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"saludo": f"¡Hola, {nombre}."}


# ==========================
#  3. EJECUCION
# ==========================
if __name__ == "__main__":
    
    '''
    ret = inicio()
    print(ret)
    '''
    uvicorn.run(app, host="127.0.0.1", port=8040)

    # con parametro reload=True, el servidor se reinicia automáticamente al detectar cambios en el código
    # uvicorn.run("main:app", host="127.0.0.1", port=8040, reload=True)
    



