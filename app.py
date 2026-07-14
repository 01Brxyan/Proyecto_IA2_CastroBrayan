import streamlit as st
import requests

# Configuración visual de la página web
st.set_page_config(page_title="DocuForm - SaaS Documental", page_icon="📄", layout="wide")

st.title("📄 DocuForm")
st.caption("Generación Formal de Documentos Administrativos con RAG Normativo")

# Inicializar la memoria del chat en la sesión web
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola Cami! ¿Qué documento administrativo deseas generar hoy?"}]

# Renderizar el historial de mensajes en la interfaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar la interacción de Cami en la web
if user_input := st.chat_input("Escribe tu solicitud aquí... (Ej: Necesito un formulario de ingreso)"):
    # Mostrar el mensaje de Cami en la pantalla
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # URL exacta de pruebas para capturar el "Execute workflow" que tienes activo en pantalla
    N8N_WEBHOOK_URL = "https://brxyan01.app.n8n.cloud/webhook-test/docuform-chat"
    
    payload = {
        "user_message": user_input,
        "usuario": "Cami",
        "session_id": "session_hub_001"
    }

    try:
        # Enviar el mensaje al backend en n8n
        res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=25)
        
        if res.status_code == 200:
            response_data = res.json()
            
            if isinstance(response_data, list) and len(response_data) > 0:
                data_dict = response_data[0]
            else:
                data_dict = response_data

            # Extraemos de la clave 'output' que vimos en tu captura
            if isinstance(data_dict, dict) and "output" in data_dict:
                bot_response = data_dict["output"]
            else:
                bot_response = f"Respuesta del servidor: {response_data}"
            
        else:
            bot_response = f"Error en el servidor de automatización (Código {res.status_code})."

        # Mostrar la respuesta del bot experto en la web
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

    except Exception as e:
        st.error(f"Ocurrió un error en la conexión: {e}")