import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Digite GOOGLE_API_KEY no arquivo .env")

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_tokens=1000
)

prompt = ChatPromptTemplate.from_template(
    "Explique o seguinte assunto para um iniciante: {assunto}"
)

chain = prompt | modelo | StrOutputParser()

resposta = chain.invoke({
    "assunto": "Agentes de inteligência artificial"
})

print(resposta)