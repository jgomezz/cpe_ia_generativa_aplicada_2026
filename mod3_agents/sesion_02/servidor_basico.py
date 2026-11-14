from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TiendaYa", log_level="ERROR")

PEDIDOS = {
    "48213": "en ruta, llega el 26/10/2026 a Arequipa",
    "50555": "en preparación, llega el 30/10/2026 a Cusco",
}

@mcp.tool()
def consultar_pedido(numero_pedido: str) -> str:
    """Consulta el estado de un pedido de TiendaYa a partir de su número."""
    return PEDIDOS.get(numero_pedido, f"No existe el pedido {numero_pedido}.")

if __name__ == "__main__":
    mcp.run(transport="stdio")
