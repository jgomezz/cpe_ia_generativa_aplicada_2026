
# Configurar Virtual Environment en Python

## Pasos de instalación

### 1. Crear el virtual environment
```bash
# python3.12 -m venv .venv
python3 -m venv .venv
```

### 2. Activar el virtual environment

**En Windows:**
```bash
# Permitir ejecutar politicas de seguridad desde consola
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activar ve
.\.venv\Scripts\activate
```

### 3. Verificar la activación
```bash
where python  # Windows
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Desactivar el virtual environment
```bash
deactivate
```
