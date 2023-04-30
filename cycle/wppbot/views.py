from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Olá mundo. Este é o index para o Chatbot do WPP")