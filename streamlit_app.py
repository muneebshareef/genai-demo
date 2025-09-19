import streamlit as st
import requests
import os

st.set_page_config(page_title="💬 Free HF Chatbot")

st.title("💬 Chatbot (Free Hugging Face Version)")
st.write(
    "This chatbot uses a free Hugging Face model instead of OpenAI. "
    "You need a Hugging Face Access Token, which you can create [here](https://huggingface.co/settings/tokens)."
)

# Ask for Hugging Face token
hf_token = st.text_input("🔑 Hugging Face Access Token", type="password")

if not hf_token:
    st.info("Please enter your Hugging Face token to continue.", icon="🗝️")
else:
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {hf_token}"}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("You:", key="user_input")

    if st.button("Send") and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            st.markdown("Thinking...")
            response = ""
            try:
                res = requests.post(API_URL, headers=headers, json={"inputs": user_input}, timeout=60)
                data = res.json()
                response = data.get("generated_text", str(data))
            except Exception as e:
                response = f"Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

    # Show chat history
    for msg in reversed(st.session_state.messages):
        if "bot" in msg:
            st.markdown(f"**Bot:** {msg['bot']}")
        else:
            st.markdown(f"**You:** {msg['user']}")
