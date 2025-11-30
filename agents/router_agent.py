import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

router_llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0
)

router_prompt = ChatPromptTemplate.from_template("""
Você é um roteador de intenções. O usuário fará uma pergunta ou um pedido.
Sua tarefa é classificar a intenção do usuário em uma das seguintes categorias:
- **pesquisa**: O usuário quer uma informação ou uma resposta a uma pergunta.
- **gerar_documento**: O usuário quer criar um documento jurídico (ex: mandado de segurança, petição, contrato).
- **enviar_email**: o usuário quer enviar um documento por email.
                                                 

Responda SOMENTE com a categoria da intenção (pesquisa ou gerar_documento ou enviar_email).
Se a intenção não for clara ou não se encaixar em nenhuma das categorias, responda "pesquisa".

Pergunta do usuário: {input}
""")

router_chain = router_prompt | router_llm | StrOutputParser()
