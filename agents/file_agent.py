import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder

from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm_document_gen = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

document_identification_prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente jurídico especializado na criação de documentos.
    Sua tarefa é identificar o tipo de documento que o usuário deseja criar (por exemplo, "mandado de segurança", "petição inicial").
    Uma vez identificado, você deve pedir as informações **mínimas e essenciais** necessárias para redigir o documento.
    Não gere o documento até ter todas as informações necessárias.

    Exemplo de interação:
    Usuário: Quero um mandado de segurança.
    Você: Ótimo! Para o mandado de segurança, preciso das seguintes informações:
    1. Nome completo e qualificação do impetrante (nome, CPF, endereço, profissão, estado civil).
    2. Nome completo e qualificação da autoridade coatora.
    3. Descrição detalhada do ato ilegal ou abusivo.
    4. Provas que fundamentam o direito líquido e certo.
    5. O pedido específico a ser formulado ao juiz.
    Por favor, forneça essas informações para que eu possa iniciar a redação.
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

document_identification_chain = document_identification_prompt | llm_document_gen | StrOutputParser()

def generate_document_content(document_type: str, document_info: str, chat_history: list):
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um redator de documentos jurídicos experiente.
        Com base no tipo de documento e nas informações fornecidas, redija o documento.
        Use linguagem jurídica formal e a estrutura padrão do documento.
        Se alguma informação essencial estiver faltando, mencione que é um placeholder
        e que o usuário deve preencher essa parte.

        Tipo de Documento: {document_type}
        Informações Detalhadas: {document_info}

        Importante: Gere apenas o texto do documento. Não inclua conversas, introduções ou finalizações extras.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", f"Gere o conteúdo completo de um(a) {document_type} com base nas informações fornecidas.")
    ])
    chain = final_prompt | llm_document_gen | StrOutputParser()
    return chain.invoke({"document_type": document_type, "document_info": document_info, "chat_history": chat_history})