from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .generate_response_message import generate_response_message

@csrf_exempt
def index(request):
	if (request.method == "POST"):
		generated_message = generate_response_message(request)
		#print(message.sid)
		# tratar se mensagem foi enviada ou não
		return HttpResponse ("Mensagem Enviada")
	else:
		return HttpResponse("Olá mundo. Este é o index para o Chatbot do WPP")