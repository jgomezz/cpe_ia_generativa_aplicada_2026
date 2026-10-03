from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env   

model = "google_genai:gemini-3.5-flash-lite"

llm = init_chat_model(model=model)

response = llm.invoke("Cual es la capital de Perú?")

print(response.text)


