from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Politicas", port=8001, log_level="ERROR")

# Datos simulados de TiendaYa
POLITICAS = {
    "devoluciones": "15 días calendario desde la entrega; 7 días para productos electrónicos.",
    "envios": "Envío gratuito desde S/ 150; envío express en Lima por S/ 24.90.",
    "cambios": "Cambios de talla o color: 30 días desde la entrega, con la etiqueta puesta.",
}

@mcp.tool()
def consultar_politica(tema: str) -> str:
    """Devuelve la política de TiendaYa sobre un tema: 'devoluciones', 'envios' o 'cambios'."""
    return POLITICAS.get(tema.lower(), "No existe una política sobre ese tema.")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
