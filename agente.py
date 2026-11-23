import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Digite GOOGLE_API_KEY no arquivo .env")

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

@tool
def consultar_pedido(numero_pedido: int) -> str:
    """Consultar o status de um pedido pelo número"""

    pedidos = {
        1024: "Pedido enviado. Previsão de entrega: amanhã.",
        1025: "Pedido em preparação.",
        1026: "Pedido entregue."
    }

    resultado = pedidos.get(numero_pedido)

    if resultado is None:
        return "Pedido não encontrado."
    
    return resultado

memoria = InMemorySaver()

agente = create_agent(
    model=modelo,
    tools=[consultar_pedido],
    system_prompt=(
        "Você é um assistente de atendimento de uma loja virtual. "
        "Quando o cliente perguntar sobre um pedido, "
        "utilize a ferramenta consultar_pedido. "
        "Nunca invente informações sobre pedidos."
    ),
    checkpointer=memoria
)

config = {
    "configurable": {
        "thread_id": "cliente-001"
    }
}

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() == "sair":
        break
    
    resultado = agente.invoke(
        {
            "messages": [
                {"role": "user", "content": pergunta}
            ]
        },

        config=config
    )

    resposta = resultado["messages"][-1].text

    print("\nAgente:", resposta)

