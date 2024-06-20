import requests
import json
import streamlit as st
import pytz
from datetime import datetime
from funtions import *

st.set_page_config(

    page_title="Wezen AI",
    page_icon="img/logo_wezen.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

with open ("./css/style.css") as f:
    st.markdown(f"<style>{f.read}</style>", unsafe_allow_html=True)

# Define o fuso horário para o Brasil (Brasília)
brasil_timezone = pytz.timezone('America/Sao_Paulo')

# Configuração do timeout para 1800 segundos
timeout_seconds = 1800
session = requests.Session()
session.timeout = timeout_seconds

st.image("img/logo_wezen.png", width=120)
st.title("Wezen AI")
st.caption("🚀 Bem Vindo a Wezen AI, inteligencia artificial da Wezen 🚀")

if "aConversation" not in st.session_state:
    st.session_state["aConversation"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "documentos" not in st.session_state:
    st.session_state["documentos"] = []
    
if "document_to_approve" not in st.session_state:
    st.session_state["document_to_approve"] = None
    
if "last_message_displayed" not in st.session_state:
    st.session_state["last_message_displayed"] = False

# Exibe as mensagens no chat
for msg in st.session_state.messages:
     st.chat_message(msg["role"],avatar=msg.get("avatar")).write(f"{msg['content']} \n\n - {msg['timestamp']}")

# Verifica se o usuário inseriu alguma mensagem no campo de entrada do chat
if prompt := st.chat_input("Como posso ajudá-lo ?"):
    
    st.session_state.messages.append({"role": "user",
                                      "content": prompt,
                                      "timestamp": datetime.now(brasil_timezone).strftime('%d/%m/%Y - %H:%M:%S')})

    ##Exibe a mensagem do usuário na interface do usuário usando o componente
    st.chat_message("user").write(f"{prompt} \n\n - "
                                  f"{datetime.now(brasil_timezone).strftime('%d/%m/%Y - %H:%M:%S')}")
    
    api_url = "https://77b1-179-191-86-210.ngrok-free.app/wezen_ai"

    headers = {
        'ngrok-skip-browser-warning': '69420',
        'Content-Type': 'application/json',
    }

    data = {
        "text": prompt,
        "memory_json": json.dumps(st.session_state.aConversation)
    }

    with st.spinner('Aguardando resposta...'):
        response = session.post(api_url, headers=headers, json=data, timeout=1800)
        mensagem_assistente = response.text
        
    st.session_state.messages.append({"role": "assistent",
                                      "content": mensagem_assistente,
                                      "timestamp": datetime.now(brasil_timezone).strftime("%d/%m/%Y - %H:%M:%S"),
                                      "avatar": "img/logo_wezen.png"})

    # Adicione a conversa atual a aConversation
    st.session_state.aConversation.append({
        "user": prompt,
        "api": mensagem_assistente
    })

    # Extrai documentos da resposta da IA
    extrair_documentos(mensagem_assistente)
    
    # Marca que a última mensagem que foi exibida
    st.session_state["last_message_displayed"] = False
          
# Exibe a última mensagem da IA e documentos para aprovação, se houver
if st.session_state.messages and not st.session_state["last_message_displayed"]:
    st.chat_message(st.session_state.messages[-1]["role"], avatar='img/logo_wezen.png').write(
        f"{st.session_state.messages[-1]['content']} \n\n - {datetime.now(brasil_timezone).strftime('%d/%m/%Y - %H:%M:%S')}"
    )
    st.session_state["last_message_displayed"] = True
    
# Exibe documentos para aprovação
if st.session_state.documentos:
    st.subheader("Documentos")
    for doc_num in st.session_state["documentos"]:
        if st.button(f"Documento Nº {doc_num}"):
            st.session_state["document_to_approve"] = doc_num
            st.rerun()
           
# Exibe o diálogo de confirmação de aprovação se um documento foi selecionado e o modal deve ser exibido
if st.session_state["document_to_approve"]:
    confirm_approval(st.session_state["document_to_approve"])
                
        

