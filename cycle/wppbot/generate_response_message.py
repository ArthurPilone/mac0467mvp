from decouple import config

import random as rd
import re

from twilio.rest import Client

from .models import ChatbotUser, Report
from ..promos.models import PartnerPromotion, SingleUsePromotionalCode, PartnerAdvert
from .report_state import *
from .messageTexts import *
from time import time

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def generate_response_message(request):
	#print(request.POST)
	receiving_no = request.POST["To"]
	user_phone = request.POST["From"]
	incoming_message = request.POST["Body"]

	userObj = ChatbotUser.objects.all().filter(user_contact_addr=user_phone)
	
	if(len(userObj) <= 0):
		userObj = ChatbotUser(user_contact_addr=user_phone)
		userObj.save()
		messageText = welcome_message_text
	else:
		userObj = userObj[0]

		if userObj.midReport:
			current_report = userObj.report_set.order_by('-dateCreated')[0]
			print(current_report.report_state)
			
			#você sabia que as funções também podem ter atributos?
			if hasattr(generate_response_message, 'lastMsgTime') and time() - generate_response_message.lastMsgTime > 86400:
				if  current_report.report_state != "ASLC" or current_report.report_state != "ASLN":
				    
					generate_response_message.next_state = current_report.report_state
				current_report.report_state = "ASLN"
				
			match current_report.report_state:
				case "AWCT":
					report_handler = ReportAwaitingCategory(current_report)
				case "AWDC":
					report_handler = ReportAwaitingDescription(current_report)
				case "CFDC":
					report_handler = ReportConfirmDescription(current_report)
				case "AWLC":
					report_handler = ReportAwaitingLocation(current_report)
				case "ASLN":
					report_handler = ReportAsleepNotify (current_report)
				case "ASLC":
					report_handler = ReportAsleepConfirm (current_report)
				case x:	
					raise Exception("Report com estado inválido: " + x)
						
			if current_report.report_state == "ASLC":
				(conclusion, messageText) = report_handler.interpret_message (incoming_message, generate_response_message.next_state)
				
			elif current_report.report_state == "AWLC":
				
				if "Latitude" not in request.POST and "Longitude" not in request.POST:
					latitude  = None
					longitude = None
				else:	
					latitude  = request.POST["Latitude"]
					longitude = request.POST["Longitude"]
					
				#nem sempre o campo Address aparece
				if "Address" not in request.POST:
					address = ""
				else:
					address = request.POST["Address"]
					
				(conclusion, messageText) = report_handler.interpret_message (latitude,
																			longitude, 
																			address)
			else:
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

		elif hasattr(generate_response_message, 'setFrequencyMode') and generate_response_message.setFrequencyMode:
		
			if incoming_message[0] in ["1", "2", "3", "4", "5", "6"]:
				generate_response_message.setFrequencyMode = False
				
			if   incoming_message[0] == "1":
				generate_response_message.promotionDelay = 86400
			elif incoming_message[0] == "2":
				generate_response_message.promotionDelay = 172800
			elif incoming_message[0] == "3":
				generate_response_message.promotionDelay = 259200
			elif incoming_message[0] == "4":
				generate_response_message.promotionDelay = 604800
			elif incoming_message[0] == "5":
				generate_response_message.promotionDelay = 1209600
			elif incoming_message[0] == "6":
				generate_response_message.promotionDelay = -1
			else:
				message_text = "Ops, não entendi." + choose_frequency 
		
		else:
			if incoming_message[0] == "1":
				messageText= prompt_category_message_text
				userObj.midReport = True
				new_report = Report(author=userObj)
				new_report.save()
				userObj.save()
			elif incoming_message[0] == "2":
				messageText = about_text
			elif incoming_message[0] == "3":
				messageText = choose_frequency
				generate_response_message.setFrequencyMode = True
			
			else:
			    messageText = welcome_back_message_text

	message = client.messages.create(
		from_=receiving_no,
		to=user_phone,
		body=messageText
	)
	generate_response_message.lastMsgTime = time()
	return message

def generate_reward_text_message(userObj):
	'''
	Gera um texto a ser adicionado ao final da resposta dada ao usuário
	para recompensá-lô com um código promocional ou anúncio 
	'''

	unused_promotional_codes = list(SingleUsePromotionalCode.objects.select_related("related_promotion").filter(used=False))
	#se alguém souber um jeito melhor de fazer isso que não envolva criar um conjunto
	#por favor me avise
	promotion_codes = set ()
	for promo_code in unused_promotional_codes:
		promotion_codes.add(promo_code.related_promotion)
	
	if(len(unused_promotional_codes) == 0) or (hasattr(generate_reward_text_message, 'lastPromotionId') and len(promotion_codes) == 1):
		adverts = list(PartnerAdvert.objects.all())
		picked_advert = rd.choice(adverts) # Escolhe um anúncio aleatoriamente
		return picked_advert.advert_text
	
	# Cheque se o usuário já recebeu código dessa promoção, e evite dar se for o caso
	# Se houver apenas uma promoção um anúncio será exibido no lugar do código promocional
	
	if hasattr(generate_reward_text_message, 'lastPromotionId'):
		possible_codes = []
		
		for promo_code in unused_promotional_codes:
			if generate_reward_text_message.lastPromotionId != promo_code.related_promotion:
				possible_codes.append (promo_code)
				
		picked_code = rd.choice(possible_codes)
	else:
		picked_code = rd.choice(unused_promotional_codes)
	
	text = picked_code.related_promotion.promotion_text
	text_with_code = re.sub("\[PROMO\_CODE\]",picked_code.code,text)

	
	picked_code.used = True
	picked_code.usedBy = userObj
	picked_code.save()
	
	#avaliable_promotions = PartnerPromotion.objects.all()
	#used_promotions_codes = SingleUsePromotionalCode.objects.filter(used=True, usedBy=userObj.id).select_related("related_promotion")
	
	generate_reward_text_message.lastPromotionId = picked_code.related_promotion
	
	
	return text_with_code
