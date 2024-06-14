import streamlit as st
import re

# Função para extrair documentos da resposta da IA
def extrair_documentos(resposta):
    pattern = r'\b45000\d+\b'
    documentos = re.findall(pattern, resposta)
    st.session_state["documentos"].extend(documentos)

@st.experimental_dialog("Documentos")
def confirm_approval(doc_num):
    st.write(f"O que deseja fazer com o documento Nº {doc_num}?")
    approve = st.button("Aprovar")
    reject = st.button("Rejeitar")
    if approve:
        st.session_state["document_to_approve"] = None
        st.rerun()
    if reject:
        st.session_state["document_to_approve"] = None
        st.rerun()


