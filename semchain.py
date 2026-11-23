import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Digite GOOGLE_API_KEY no arquivo .env")

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

resposta = modelo.invoke("O que é inteligência articial?")

print(resposta.text)