import json
from uuid import uuid4

from django.http import JsonResponse
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph

from nova_vida_ia import settings
from nova_vida_ia.chatbot.memory import ChromaDB


class Chatbot:
    def __init__(self, request):
        self.chatbot_model = settings.CHATBOT_MODEL
        self.client = ChatGroq(api_key=settings.API_KEY, model_name=self.chatbot_model, temperature=0.3)
        self.request_data = json.loads(request.body.decode())
        self.vector_db = ChromaDB()
        self.graph = StateGraph(state_schema=MessagesState)

        with open('./nova_vida_ia/chatbot/prompts/prompt_template.txt', 'r') as file:
            self.system_prompt = file.read()

    def message(self):
        event_chats = []
        user_msg = self.request_data['user_msg']
        user_preferences = self.vector_db.get_user_preferences()
        previous_data = self.vector_db.get_previous_data()
        graph = self.graph

        graph.add_edge(START, "client")
        graph.add_node("client", self.invoke_client)
        app = graph.compile()

        config = {"configurable": {"thread_id": uuid4()}}

        template = (f"Seu Template: {self.system_prompt}\n"
                    f"Memórias: {' '.join(previous_data)}\n"
                    f"Preferências do usuário: {user_preferences}")

        system_message = SystemMessage(content=template)
        input_message = HumanMessage(content=user_msg)

        for event in app.stream({"messages": [system_message, input_message]}, config, stream_mode="values"):
            event_chats.append(event["messages"][-1])

        assistant_response = event_chats[-1].content

        self.vector_db.store_user_preferences(user_msg, self.client, self.chatbot_model)
        self.vector_db.create_memory(assistant_response, user_msg)

        return JsonResponse({
            "response_message": assistant_response
        })

    def invoke_client(self, state: MessagesState):
        response = self.client.invoke(state["messages"])

        return {"messages": response}
