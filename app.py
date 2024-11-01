import json

import requests
import streamlit as st

from nova_vida_ia import settings

st.title("Nova Vida ChatBot")

prompt = st.chat_input("user")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    response = requests.post(f"{settings.CHATBOT_URL}/api/chatbot/message", json={"user_msg": prompt})

    if response.ok:
        with st.chat_message("assistant"):
            message = json.loads(response.content)
            st.write(message.get("response_message"))
