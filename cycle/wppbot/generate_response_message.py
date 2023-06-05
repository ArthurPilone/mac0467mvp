from decouple import config

import random as rd
import re

from twilio.rest import Client

from .models import ChatbotUser, Report
from ..promos.models import PartnerPromotion, SingleUsePromotionalCode, PartnerAdvert
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
				case x:	
					raise Exception("Report com estado inválido: " + x)

			(conclusion, messageText) = report_handler.interpret_message(incoming_message)

			match conclusion:
				case "ABORT":
					userObj.midReport = False
					userObj.save()
				case "REWARD":
					userObj.midReport = False
					userObj.save()

					# Montar mensagem com recompensa
					reward_text = generate_reward_text_message(userObj)
					
					messageText += reward_text

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

def generate_reward_text_message(userObj):
	'''
	Gera um texto a ser adicionado ao final da resposta dada ao usuário
	para recompensá-lô com um código promocional ou anúncio 
	'''

	unused_promotional_codes = list(SingleUsePromotionalCode.objects.select_related("related_promotion").filter(used=False))

	if(len(unused_promotional_codes) == 0):
		adverts = list(PartnerAdvert.objects.all())
		picked_advert = rd.choice(adverts) # Escolhe um anúnio aleatoriamente
		return picked_advert.advert_text
	
	picked_code = rd.choice(unused_promotional_codes)
	text = picked_code.related_promotion.promotion_text
	text_with_code = re.sub("\[PROMO\_CODE\]",picked_code.code,text)

	picked_code.used = True
	picked_code.usedBy = userObj
	picked_code.save()

	return text_with_code

	# Checar se usuário já recebeu código dessa promoção, e evitar dar 
	#avaliable_promotions = PartnerPromotion.objects.all()
	#used_promotions_codes = SingleUsePromotionalCode.objects.filter(used=True, usedBy=userObj.id).select_related("related_promotion")