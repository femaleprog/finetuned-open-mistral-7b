import streamlit as st
import requests

def main():
    # Backend API URL
    API_URL = "http://localhost:8000/chat/"

    # Streamlit UI Setup
    st.title("🗨️ Mistral Chatbot")

    # Session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send request to FastAPI backend
        response = requests.post(API_URL, json={"text": user_input})
        bot_reply = response.json().get("response", "Error: No response from server.")

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
if __name__ == "__main__":
    main()