from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

email_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

email_prompt = ChatPromptTemplate.from_template("""
Você é um agente especializado em envio de documentos por email.
Sua função é perguntar ao usuário **qual é o email de destino**.

Se o usuário ainda não forneceu o email, pergunte: 
"Para qual endereço de email deseja enviar o documento?"

Se o usuário já forneceu o email, responda somente: "OK".
Pergunta do usuário: {input}
""")

email_chain = email_prompt | email_llm | StrOutputParser()
