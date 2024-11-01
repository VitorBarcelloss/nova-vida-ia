import json
from uuid import uuid4

import chromadb

from nova_vida_ia import settings


class ChromaDB:
    def __init__(self):
        self.vector_db = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
        self.collection = self.vector_db.get_or_create_collection("chatbot_memory")

    def get_user_preferences(self):
        preferences = []
        memory = self.collection.get()

        for doc in memory.get('documents'):
            json_doc = json.loads(doc)
            if json_doc['metadata']['role'] == 'user_preferences':
                preferences.append(json_doc['content'])

        return preferences

    def get_previous_data(self):
        previous_data = []
        memory = self.collection.get()

        for doc in memory.get('documents'):
            json_doc = json.loads(doc)
            if json_doc['metadata']['role'] != 'user_preferences':
                previous_data.append(json_doc['content'])

        return previous_data

    def store_user_preferences(self, user_message, client, chatbot_model):
        preferences_prompt = (f"Detecte as preferencias do usuario nesta mensagem e somente liste elas, "
                              f"se não houver nenhuma preferencia, não retorne nada: {user_message}")

        try:
            response = client.invoke(preferences_prompt)

            if response.content != 'Nenhuma preferência detectada.':
                documents = json.dumps({
                    "content": response.content.replace('\n', ' '),
                    "metadata": {"role": "user_preferences"}
                })

                self.collection.add(
                    ids=[str(uuid4())],
                    documents=[documents]
                )
        except Exception as e:
            print(e)

    def create_memory(self, ai_message, user_message):
        ai_message = json.dumps({
            "content": ai_message,
            "metadata": {"role": "assistant"}
        })

        user_message = json.dumps({
            "content": user_message,
            "metadata": {"role": "user_msg"}
        })

        self.collection.add(
            ids=[str(uuid4()), str(uuid4())],
            documents=[ai_message, user_message]
        )



