import streamlit as st
import re

# Função para extrair documentos da resposta da IA
def extrair_documentos(resposta):
    pattern = r'\b45000\d+\b'
    documentos = re.findall(pattern, resposta)
    for doc in documentos:
        if doc not in st.session_state["documentos"]:
            st.session_state["documentos"].append(doc)

@st.experimental_dialog("Documentos")
def confirm_approval(doc_num):
    st.write(f"O que deseja fazer com o documento Nº {doc_num}?")
    
    motivo = st.text_input("Motivo:")
    
    col1, col2, _ = st.columns([1, 1, 3])
    
    with col1:
        approve = st.button("Aprovar")
    with col2:
        reject = st.button("Rejeitar")
    
    if approve:
        st.session_state["document_to_approve"] = None
         # Remove o documento do vetor de documentos
        if doc_num in st.session_state["documentos"]:
            st.session_state["documentos"].remove(doc_num)
        st.rerun()
    if reject:
        st.session_state["document_to_approve"] = None
         # Remove o documento do vetor de documentos
        if doc_num in st.session_state["documentos"]:
            st.session_state["documentos"].remove(doc_num)
        st.rerun()

    
