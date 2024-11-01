from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from nova_vida_ia.chatbot.chatbot import Chatbot

@csrf_exempt
def message(request):
    if request.method != "POST":
        raise ...
    return Chatbot(request).message()

@csrf_exempt
def chat_view(request):
    return render(request, 'index.html')