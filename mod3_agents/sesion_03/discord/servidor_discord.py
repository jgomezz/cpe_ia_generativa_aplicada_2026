import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("Discord", port=8002, log_level="ERROR")

#
@mcp.tool()
def enviar_mensaje(texto: str) -> str:
    """Envía un mensaje a un canal de Discord usando un webhook."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return "No se ha configurado la URL del webhook de Discord."
    
    payload = {"content": texto}
    try:
        response = httpx.post(webhook_url, json=payload)
        response.raise_for_status()
        return "Mensaje enviado correctamente a Discord."
    except httpx.HTTPError as e:
        return f"Error al enviar el mensaje a Discord: {e}"

#
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
