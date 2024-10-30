import json

import chromadb
from django.http import JsonResponse
from groq import Groq

from nova_vida_ia import settings
from nova_vida_ia.chatbot.memory import ChromaDB


class Chatbot:
    def __init__(self, request):
        self.client = Groq(api_key=settings.API_KEY)
        self.chatbot_model = settings.CHATBOT_MODEL
        self.request_data = json.loads(request.body.decode())
        self.vector_db = ChromaDB()

        with open('./nova_vida_ia/chatbot/prompts/prompt_template.txt', 'r') as file:
            self.system_prompt = file.read()


    def message(self):
        user_msg = self.request_data['user_msg']
        messages = self.get_messages(user_msg)

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.chatbot_model,
            temperature=0.6,
            max_tokens=2048,
            top_p=0.5,
            stop=None,
            stream=False
        )

        assistant_response = chat_completion.choices[0].message.content
        self.vector_db.create_memory(assistant_response, "assistant")
        self.vector_db.create_memory(user_msg, "user")

        return JsonResponse({
                "response_message":chat_completion.choices[0].message.content
            })

    def get_messages(self, user_msg):
        previous_message = self.vector_db.get_previous_messages()
        messages = [
            {
                "role": "user",
                "content": user_msg,
            },
            {
                "role": "system",
                "content": self.system_prompt,
            }]

        return previous_message + messages
