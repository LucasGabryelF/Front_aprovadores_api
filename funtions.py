import streamlit as st
import dotenv
import os
import requests
import json
import re

dotenv.load_dotenv(dotenv.find_dotenv())

api_url = os.getenv("UrlOdata")

headers = {
    'ngrok-skip-browser-warning': '69420',
    'Content-Type': 'application/json',
}

# Função para extrair documentos da resposta da IA
def extrair_documentos(resposta):
    pattern = r'\b45000\d+\b'
    documentos = re.findall(pattern, resposta)
    for doc in documentos:
        if doc not in st.session_state["documentos"]:
            st.session_state["documentos"].append(doc)

@st.experimental_dialog("Documentos")
def confirm_approval(doc_num, aprovador):
    st.write(f"O que deseja fazer com o documento Nº {doc_num}?")
    
    motivo = st.text_input("Motivo:")
    
    col1, col2, _ = st.columns([1, 1, 3])
    
    with col1:
        approve = st.button("Aprovar")
    with col2:
        reject = st.button("Rejeitar")
    
    if approve or reject:
        status = "APPROVED" if approve else "REJECTED"
        print(status)
        data = {
            "aprovador": aprovador,
            "documento": doc_num,
            "status": status,
            "motivo": motivo
        }
        
        print(data)
        
        with st.spinner('Aguardando resposta...'):
            response = requests.post(api_url, headers=headers, json=data, timeout=1800)
            if response.status_code == 200:
                response_data = response.json()
                if isinstance(response_data, list) and len(response_data) > 0 and 'MSG' in response_data[0]:
                    st.success(f"Operação realizada com sucesso! Resposta: {response_data[0]['MSG']}")
            else:
                st.error("Erro na operação!")
        
        #st.session_state["document_to_approve"] = None
        #if doc_num in st.session_state["documentos"]:
            #st.session_state["documentos"].remove(doc_num)
        #st.rerun()

    
