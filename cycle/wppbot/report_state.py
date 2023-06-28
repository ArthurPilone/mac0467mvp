from .models import Report
from .messageTexts import *

class ReportState():
	"""
	Classe 'abstrata' para o tratamento de uma denúncia em um dado estado
	"""

	def __init__(self, corresponding_report : Report):
		'''
		Constrói objeto relacionado à denúncia e salva internamente 
		modelo Report correspondente
		'''
		raise NotImplementedError
		

	def interpret_message(self,message: str) -> tuple[bool, str]:
		'''
		Interpreta mensagem dada pelo usuário, atualiza
		internamente o objeto Report do BD, e uma tupla com o novo
		valor de usuário.midReport e a resposta a ser enviada ao cliente.
		'''
		raise NotImplementedError

class ReportAwaitingCategory(ReportState):
	"""
	Classe que trata uma denúncia recém aberta que aguarda categoria
	"""

	def __init__(self, corresponding_report : Report):
		'''
		Constrói objeto relacionado à denúncia e salva internamente 
		modelo Report correspondente
		'''

		self.report = corresponding_report

	def interpret_message(self, message: str) -> tuple[bool, str]:
		'''
		Interpreta mensagem dada pelo usuário, atualiza
		internamente o objeto Report do BD, e devolve a 
		resposta a ser enviada ao cliente.
		'''

		if(message[0] in ['1', '2', '3', '4', '5', '6']):
			match message[0]:
				case '1':
					self.report.categoria = "Sinalização"
				case '2':
					self.report.categoria = "Iluminação"
				case '3':
					self.report.categoria = "Segurança"
				case '4':
					self.report.categoria = "Acessibilidade"
				case '5':
					self.report.categoria = "Manutenção da Via"
				case '6':
					self.report.categoria = "Outros"
			
			self.report.report_state = "AWDC"
			self.report.save()
			return ("CONTINUE", "Ok." + prompt_description_message_text)
		
		elif(message[0:4] == "Sair" or message[0:4] == 'sair'):
			self.report.delete()
			return ("ABORT", "Denúncia cancelada com sucesso!")
		else:
			return ("CONTINUE", "Ops, não entendi." + prompt_category_message_text)

class ReportAwaitingDescription(ReportState):
	"""
	Classe que trata uma denúncia que espera a descrição do usuário
	"""

	def __init__(self, corresponding_report : Report):
		'''
		Constrói objeto relacionado à denúncia e salva internamente 
		modelo Report correspondente
		'''

		self.report = corresponding_report

	def interpret_message(self, message: str) -> tuple[bool, str]:
		'''
		Interpreta mensagem dada pelo usuário, atualiza
		internamente o objeto Report do BD, e devolve a 
		resposta a ser enviada ao cliente.
		'''

		if(message[0:4] == "Sair" or message[0:4] == 'sair'):
			self.report.delete()
			return ("ABORT", "Denúncia cancelada com sucesso!")
		else:
			if(len(message) > 500):
				return("CONTINUE", "Ops, sua descrição é muito longa." + prompt_description_message_text)
			self.report.description = message
			self.report.report_state = "CFDC"
			self.report.save()
			return ("CONTINUE", "OK." + prompt_confirm_description(message))

class ReportConfirmDescription(ReportState):
	"""
	Classe que trata uma denúncia que foi dada uma descrição pelo usuário
	e agora aguarda sua confirmação .
	"""

	def __init__(self, corresponding_report : Report):
		'''
		Constrói objeto relacionado à denúncia e salva internamente 
		modelo Report correspondente
		'''

		self.report = corresponding_report

	def interpret_message(self, message: str) -> tuple[bool, str]:
		'''
		Interpreta mensagem dada pelo usuário, atualiza
		internamente o objeto Report do BD, e devolve a 
		resposta a ser enviada ao cliente.
		'''

		if(message[0] == '1'):
			self.report.report_state = "DONE" # Aqui trocar pra aguardando lcoalização
			self.report.save()
			return ("REWARD", present_reward_message_text)
		elif(message[0] == '2'):
			self.report.report_state = "AWDC"
			self.report.save()
			return ("CONTINUE", "Ok." + prompt_description_message_text)
		elif(message[0:4] == "Sair" or message[0:4] == 'sair'):
			self.report.delete()
			return ("ABORT", "Denúncia cancelada com sucesso!")
		else:
			return ("CONTINUE", "Ops, não entendi." + prompt_confirm_description(self.report.description))

		#if()
