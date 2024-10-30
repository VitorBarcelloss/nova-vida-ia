import json
from uuid import uuid4

import chromadb
from chromadb import Settings


class ChromaDB:
    def __init__(self):
        self.vector_db = chromadb.HttpClient(host='localhost', port=8001)
        self.collection = self.vector_db.get_or_create_collection("chatbot_memory")

    def get_previous_messages(self):
        previous_messages = []
        memory = self.collection.get()

        for doc in memory.get('documents'):
            json_doc = json.loads(doc)

            previous_messages.append({
                "role": json_doc['metadata']['role'],
                "content": json_doc['content']
            })

        return previous_messages

    def create_memory(self, content, role):
        embedding = self.create_embedding(content)
        documents = {
            "content": content,
            "metadata": {"role": role}
        }
        json_documents = json.dumps(documents)

        self.collection.add(
            ids=[str(uuid4())],
            documents=[json_documents],
            embeddings=[embedding]
        )

    #TODO criar embedding
    def create_embedding(self, content):
        return [0.1] * 768
