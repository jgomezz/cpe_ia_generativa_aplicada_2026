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

# ==========================
#  3. EJECUCION
# ==========================
if __name__ == "__main__":
    
    '''
    ret = inicio()
    print(ret)
    '''
    uvicorn.run(app, host="127.0.0.1", port=8040)


