from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from decouple import config

from twilio.rest import Client

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@csrf_exempt
def index(request):
	print(request.method)
	if request.method == "GET" :
		return HttpResponse("Olá mundo. Este é o get para o Chatbot do WPP")
	elif (request.method == "POST"):
		receiving_no = request.POST["To"]
		user_phone = request.POST["From"]
		message = client.messages.create(
			from_=receiving_no,
			to=user_phone,
			body="Oi de volta, " + request.POST['ProfileName']  + "! "
		)
		#print(message.sid)
		return HttpResponse ("Enviei") #Trocar isso pra status code
	else:
		return HttpResponse("Olá mundo. Este é o index para o Chatbot do WPP")