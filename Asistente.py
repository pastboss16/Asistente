import streamlit as st
import google.generativeai as genai

# Configurar la API Key
GEMINI_API_KEY = "AIzaSyAc2lYPWGHOyuhANQNtab4HAFVAp5XBbPc"
genai.configure(api_key=GEMINI_API_KEY)

# Nombre del modelo
MODEL = "models/gemini-1.5-flash"

# Configuración de la página
st.set_page_config(page_title="Asistente de Apnea del Sueño", page_icon="💤")

# Título y descripción
st.title("💤 Asistente Virtual sobre Apnea del Sueño")
st.subheader("Cuéntame tus síntomas y te ayudaré a comprender si pueden estar relacionados con esta condición.")

# Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola 💤, soy tu asistente virtual. Estoy aquí para hablar contigo sobre síntomas relacionados con la apnea del sueño. Puedes contarme cómo te sientes, y te ayudaré a entender mejor tu situación. ¿Qué síntomas estás presentando?"}
    ]

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Describe tus síntomas aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            contexto = """
            La apnea del sueño es un trastorno común en el que la respiración se detiene y comienza repetidamente durante el sueño. 
            Los síntomas incluyen: ronquidos fuertes, pausas en la respiración observadas durante el sueño, somnolencia diurna, 
            dolor de cabeza al despertar, dificultad para concentrarse, irritabilidad, insomnio y sequedad en la boca al despertar.
            """

            historial = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

            model = genai.GenerativeModel(MODEL)
            response = model.generate_content(
                f"Eres un asistente virtual empático y cuidadoso que ayuda a los usuarios a entender si sus síntomas están relacionados con la apnea del sueño. "
                f"Usa esta información de contexto médico:\n{contexto}\n\n"
                f"Historial de conversación:\n{historial}\n\n"
                f"Responde con amabilidad, claridad, sin dar un diagnóstico médico, e indica la importancia de consultar con un profesional de salud."
            )
            
            respuesta = response.text if hasattr(response, 'text') else "Lo siento, no pude procesar tu solicitud."
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")
            st.session_state.messages.append(
                {"role": "assistant", "content": "Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo."}
            )

# Botón para reiniciar
if st.button("🔄 Reiniciar conversación"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola 💤, soy tu asistente virtual. Estoy aquí para hablar contigo sobre síntomas relacionados con la apnea del sueño. Puedes contarme cómo te sientes, y te ayudaré a entender mejor tu situación. ¿Qué síntomas estás presentando?"}
    ]
    st.experimental_rerun()
