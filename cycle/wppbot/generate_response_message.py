from decouple import config

from twilio.rest import Client

from .models import ChatbotUser

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def generate_response_message(request):
	print(request.POST)
	receiving_no = request.POST["To"]
	user_phone = request.POST["From"]
	
	userObj = ChatbotUser.objects.all().filter(user_contact_addr=user_phone)

	### Se usuário enviar localização, POST tem as chaves:
	# 'Latitude': ['-23.705187982804414']
	# 'Longitude': ['-46.55229829251766']
	# 'Address': ['R. Príncipe Humberto, 2 - Vila Campestre, São Bernardo do Campo - SP, 09725-200, Brasil']

	if(len(userObj) <= 0):
		userObj = ChatbotUser(user_contact_addr=user_phone)
		userObj.save()
		messageText = "Olá, seja bem-vindo ao serviço de chatbot :)" 
	else:
		userObj = userObj[0]
		messageText = "Olá de volta :)"

	message = client.messages.create(
		from_=receiving_no,
		to=user_phone,
		body=messageText
	)

	return message