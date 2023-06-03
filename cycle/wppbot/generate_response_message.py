from decouple import config

from twilio.rest import Client

from .models import ChatbotUser, Report
from .report_state import *
from .messageTexts import *

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def generate_response_message(request):
	# print(request.POST)
	receiving_no = request.POST["To"]
	user_phone = request.POST["From"]
	incoming_message = request.POST["Body"]

	userObj = ChatbotUser.objects.all().filter(user_contact_addr=user_phone)

	### Se usuário enviar localização, POST tem as chaves:
	# 'Latitude': ['-23.705187982804414']
	# 'Longitude': ['-46.55229829251766']
	# 'Address': ['R. Príncipe Humberto, 2 - Vila Campestre, São Bernardo do Campo - SP, 09725-200, Brasil']

	if(len(userObj) <= 0):
		userObj = ChatbotUser(user_contact_addr=user_phone)
		userObj.save()
		messageText = welcome_message_text
	else:
		userObj = userObj[0]

		if userObj.midReport:

			## Aqui seria interessante checar se realmente é uma denúncia recente
			# se ele começou a mais de um dia, esqueço ela
			current_report = userObj.report_set.order_by('-dateCreated')[0]
			print(current_report.report_state)

			match current_report.report_state:
				case "AWCT":
					report_handler = ReportAwaitingCategory(current_report)
				case "AWDC":
					report_handler = ReportAwaitingDescription(current_report)
				case "CFDC":
					report_handler = ReportConfirmDescription(current_report)
				case "AWLC":
					current_report.report_state = "DONE"
					userObj.midReport = False
					current_report.save()
					userObj.save()
					raise Exception("Report com estado inválido: " + "AAAAA")
				case x:	
					raise Exception("Report com estado inválido: " + x)

			(new_midReport, messageText) = report_handler.interpret_message(incoming_message)

			if(new_midReport == False):
				userObj.midReport = False
				userObj.save()

		else:
			if incoming_message[0] == "1":
				messageText= prompt_category_message_text
				userObj.midReport = True
				new_report = Report(author=userObj)
				new_report.save()
				userObj.save()
			else:
				messageText = welcome_back_message_text

	message = client.messages.create(
		from_=receiving_no,
		to=user_phone,
		body=messageText
	)

	return message