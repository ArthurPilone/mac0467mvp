
welcome_message_text = \
"""Olá, seja bem-vindo ao serviço de deúncias do CycleSpot :)
Para fazer uma denúncia, digite 1.
Para saber mais sobre o Bot do CycleSpot, digite 2.
""" 

welcome_back_message_text = \
"""Olá de volta ao serviço de deúncias do CycleSpot
Para fazer uma denúncia, digite 1.
Para saber mais sobre o Bot do CycleSpot, digite 2.
""" 

# Escolher categorias para história 1.e (sprint2)
prompt_category_message_text = \
"""
Ok, vamos começar. Qual o tipo de problema?

Digite:
'1' para problemas de Sinalização
'2' para problemas 
'Sair' para cancelar a denúncia
"""

prompt_description_message_text = \
"""
Por favor, deixe uma curta descrição do problema.
"""

prompt_confirm_description_options = \
"""
Digite:
'1' para aceitar esta descrição
'2' para escrever outra descrição
'Sair' para cancelar a denúncia
"""

def prompt_confirm_description(oldDescription):
    return "A descrição da sua denúncia será: \n'" + oldDescription + "'\n" + prompt_confirm_description_options

# Aqui, é legal deixar um link ajudando, talvez
prompt_location_message_text = \
"""
Utilize o WhatsApp para enviar a localização de onde encontrou o problema.
"""

present_reward_message_text = \
"""
Agradecemos sua denúncia. Fique com a dica de um dos nossos parceiros:\n
"""