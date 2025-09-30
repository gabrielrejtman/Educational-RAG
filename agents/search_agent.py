import os
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from tools.scraper import load_vectorstore

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

prompt = ChatPromptTemplate.from_template("""
    Você é um agente de pesquisa do Sistema Judiciário Brasileiro. Escreva sempre em português e entregue respostas somente com base no contexto fornecido. Se possível, sempre cite as fontes. Se a resposta não estiver no contexto, responda que não sabe.
    <context>
    {context}
    </context>

    Question: {input}""")

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={'k': 8})
chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
retrieval_chain = create_retrieval_chain(retriever, chain)