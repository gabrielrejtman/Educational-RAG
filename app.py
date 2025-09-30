import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage

from tools.scraper import load_vectorstore
from agents.search_agent import retrieval_chain
from agents.file_agent import document_identification_chain, generate_document_content
from tools.pdf_creator import create_pdf_from_text
from agents.router_agent import router_chain

st.set_page_config(page_title="Chat Jurídico")
st.title("Chat Jurídico - Sistema Judiciário Brasileiro")

with st.spinner("Carregando base de conhecimento..."):
    vectorstore = load_vectorstore()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_generation_state" not in st.session_state:
    st.session_state.document_generation_state = {
        "active": False,
        "document_type": None,
        "collected_info": ""
    }

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        if isinstance(msg["content"], str):
            st.chat_message("assistant").write(msg["content"])
        elif isinstance(msg["content"], dict) and msg["content"].get("type") == "pdf_link":
            st.chat_message("assistant").write("Seu documento foi gerado!")
            with open(msg['content']['path'], "rb") as file:
                st.download_button(
                    label="Baixar PDF",
                    data=file,
                    file_name=os.path.basename(msg['content']['path']),
                    mime="application/pdf",
                    key=f"download_pdf_{msg['content']['path']}"
                )

user_input = st.chat_input("Digite sua pergunta ou pedido aqui...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    chat_history_for_langchain = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_history_for_langchain.append(HumanMessage(content=msg["content"]))
        else:
            if isinstance(msg["content"], str):
                 chat_history_for_langchain.append(AIMessage(content=msg["content"]))
            
    if st.session_state.document_generation_state["active"]:
        doc_state = st.session_state.document_generation_state
        doc_state["collected_info"] += "\n" + user_input

        with st.spinner("Processando informações para gerar o documento..."):
            try:
                document_content = generate_document_content(
                    document_type=doc_state["document_type"],
                    document_info=doc_state["collected_info"],
                    chat_history=chat_history_for_langchain
                )
                
                filename = f"{doc_state['document_type'].replace(' ', '_')}_{len(st.session_state.messages)}.pdf"
                pdf_path = create_pdf_from_text(document_content, filename, doc_state['document_type'].title())

                llm_response = {
                    "type": "pdf_link",
                    "path": pdf_path,
                    "content": document_content
                }
                st.session_state.messages.append({"role": "assistant", "content": llm_response})
                st.rerun() 

                st.session_state.document_generation_state = {
                    "active": False,
                    "document_type": None,
                    "collected_info": ""
                }

            except Exception as e:
                answer = f"Erro ao gerar o documento: {e}"
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.error(answer)
            
    else:
        with st.spinner("Analisando sua intenção..."):
            intention = router_chain.invoke({"input": user_input})
            
            if intention.strip().lower() == "gerar_documento":
                with st.spinner("Preparando para gerar o documento..."):
                    response = document_identification_chain.invoke({
                        "input": user_input,
                        "chat_history": chat_history_for_langchain
                    })
                    
                    if "mandado de segurança" in user_input.lower():
                        doc_type = "Mandado de Segurança"
                    elif "petição inicial" in user_input.lower():
                        doc_type = "Petição Inicial"
                    else:
                        doc_type = "Documento Jurídico Genérico"

                    st.session_state.document_generation_state["active"] = True
                    st.session_state.document_generation_state["document_type"] = doc_type
                    st.session_state.document_generation_state["collected_info"] = user_input

                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.chat_message("assistant").write(response)

            elif intention.strip().lower() == "pesquisa":
                with st.spinner("Buscando resposta..."):
                    try:
                        result = retrieval_chain.invoke({"input": user_input})
                        llm_response = result["answer"]
                        st.session_state.messages.append({"role": "assistant", "content": llm_response})
                        st.chat_message("assistant").write(llm_response)

                        with st.expander("Fontes Consultadas"):
                            for doc in result["context"]:
                                st.write(f"**Fonte:** {doc.metadata.get('source', 'N/A')}")
                                st.caption(doc.page_content[:200] + "...")

                    except Exception as e:
                        answer = f"Erro ao processar sua pergunta: {e}"
                        st.error(answer)

            else:
                with st.spinner("Buscando resposta (intenção não clara)..."):
                    try:
                        result = retrieval_chain.invoke({"input": user_input})
                        llm_response = result["answer"]
                        st.session_state.messages.append({"role": "assistant", "content": llm_response})
                        st.chat_message("assistant").write(llm_response)
                    except Exception as e:
                        answer = f"Erro ao processar sua pergunta: {e}"
                        st.error(answer)
