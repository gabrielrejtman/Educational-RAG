import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
user_agent = os.getenv("USER_AGENT")
websites = ["https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
            "https://en.wikipedia.org/wiki/Brazilian_Constitution_of_1988",
            "https://www.planalto.gov.br/ccivil_03/leis/2002/L10406.htm",
            "https://www.planalto.gov.br/ccivil_03/leis/1940/L2848.htm",
            "https://www.planalto.gov.br/ccivil_03/leis/l8069.htm",
            "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"
            ]
PERSIST_DIR = "faiss_index"

def create_vectorstore(websites, persist_dir=PERSIST_DIR):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    loader = WebBaseLoader(websites, header_template={"User-Agent": user_agent}, requests_per_second=1)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(docs, embeddings) 
    vectorstore.save_local(persist_dir)
    return vectorstore

def load_vectorstore(persist_dir=PERSIST_DIR):
    if not os.path.exists(PERSIST_DIR):
        vectorstore = create_vectorstore(websites, persist_dir)
        return vectorstore
    else:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
        return vectorstore
    