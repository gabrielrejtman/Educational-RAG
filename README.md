# ⚖️ Chat Jurídico Brasileiro - RAG e Geração de Documentos

Este projeto implementa um sistema avançado de *Retrieval-Augmented Generation* (RAG) para o domínio jurídico brasileiro, utilizando uma base de conhecimento em leis federais (Constituição, Código Civil, etc.). Além de responder a perguntas com base no contexto (RAG), o sistema possui um segundo agente especializado em **gerar rascunhos de documentos jurídicos** (como mandados de segurança) em formato PDF.

-----

## 🚀 Funcionalidades Principais

  * **RAG (Pesquisa Jurídica):** Responde a perguntas complexas sobre o Sistema Judiciário Brasileiro com base em leis e códigos, sempre citando as fontes consultadas.
  * **Geração de Documentos:** Possui um agente de roteamento que detecta a intenção de criar um documento e inicia um fluxo de coleta de informações para gerar o rascunho do documento em **PDF**.
  * **Tecnologias Modernas:** Utiliza **LangChain** para orquestração, **Groq** (Llama 3.1) para inferência rápida e **Ollama** para *embeddings* locais.
  * **Interface Interativa:** Desenvolvido com **Streamlit** para uma experiência de chat amigável e intuitiva.

-----

## 🛠️ Configuração do Ambiente

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

### 1\. Pré-requisitos

Você deve ter os seguintes softwares instalados:

  * **Python 3.8+**
  * **Ollama:** Necessário para rodar o modelo de *embeddings* localmente.

### 2\. Instalação do Ollama

1.  Instale o [Ollama](https://ollama.com/) em seu sistema operacional.
2.  Após a instalação, baixe o modelo de *embeddings* no seu terminal:
    ```bash
    ollama pull nomic-embed-text
    ```

### 3\. Setup do Projeto

Crie e navegue até o diretório do seu projeto:

```bash
mkdir chat_juridico
cd chat_juridico
```

Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate
```

### 4\. Instalação das Dependências

Instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 5\. Configuração das Chaves de API

Crie um arquivo chamado **`.env`** na raiz do seu projeto e preencha com sua chave do Groq e a configuração do *User Agent*:

```env
# Obtenha sua chave em https://console.groq.com/keys
GROQ_API_KEY="SUA_CHAVE_GROQ_AQUI"

# User Agent para evitar bloqueios ao raspar sites do Planalto
USER_AGENT="Mozilla/5.0 (compatible; LegalChatBot/1.0;)" 
```

-----

## ▶️ Como Rodar o Aplicativo

1.  Certifique-se de que o **Ollama está em execução** no *background*.

2.  Certifique-se de que seu ambiente virtual (`venv`) está ativado.

3.  Execute o aplicativo Streamlit no terminal:

    ```bash
    streamlit run app.py
    ```

O aplicativo será aberto automaticamente no seu navegador.

### Processo Inicial (Importante\!)

Na primeira execução, o sistema fará a raspagem dos sites jurídicos e criará a base de conhecimento (índice vetorial). Este processo é indicado pelo *spinner* **"Carregando base de conhecimento..."** e pode levar alguns minutos.

Após a conclusão, a base será salva na pasta **`faiss_index`**, e as execuções futuras serão significativamente mais rápidas.

-----

## 🗺️ Arquitetura do Código (Visão Geral)

| Arquivo | Função | Componentes LangChain |
| :--- | :--- | :--- |
| **`app.py`** | Interface do usuário e lógica de roteamento principal. | - |
| **`router_agent.py`** | Classifica a intenção do usuário (`pesquisa` ou `gerar_documento`). | `ChatGroq`, `ChatPromptTemplate` |
| **`scraper.py`** | Cria e carrega o *Vector Store* (base de conhecimento). | `WebBaseLoader`, `OllamaEmbeddings`, `FAISS`, `RecursiveCharacterTextSplitter` |
| **`search_agent.py`** | Agente de RAG (Busca e Geração de Resposta). | `ChatGroq`, `create_retrieval_chain` |
| **`file_agent.py`** | Agente de Redação (Solicita info e gera o texto do documento). | `ChatGroq`, `ChatPromptTemplate` |
| **`pdf_creator.py`** | Converte o texto gerado pelo LLM em um arquivo PDF. | `fpdf2` |

-----

## 📝 Como Usar

### Modo Pesquisa (RAG)

Pergunte sobre leis, artigos ou conceitos jurídicos.

**Exemplo:**

> "Quais são os crimes inafiançáveis segundo a Constituição Federal?"

### Modo Geração de Documentos

Peça a criação de um documento. O agente irá iniciar um diálogo para coletar os dados necessários.

**Exemplo:**

> "Preciso gerar um mandado de segurança urgente."

O assistente responderá pedindo informações específicas. Você deve fornecer essas informações nas mensagens seguintes. O PDF será gerado quando o agente sentir que possui informações suficientes.
