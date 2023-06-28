
welcome_message_text = \
"""Olá, seja bem-vindo ao serviço de deúncias do CycleSpot :)
Para fazer uma denúncia, digite 1.
Para saber mais sobre o Bot do CycleSpot, digite 2.
Para configurar a frequência das ofertas que você pode receber periodicamente, digite 3.
""" 

welcome_back_message_text = \
"""Olá de volta ao serviço de deúncias do CycleSpot
Para fazer uma denúncia, digite 1.
Para saber mais sobre o Bot do CycleSpot, digite 2.
Para configurar a frequência das ofertas que você pode receber periodicamente, digite 3.
""" 

prompt_category_message_text = \
"""
Ok, vamos começar. Qual o tipo de problema?

Digite:
'1' para problemas de Sinalização
'2' para problemas de Iluminação
'3' para problemas de Segurança
'4' para problemas de Acessibilidade
'5' para problemas de Manutenção da via
'6' para problemas que não estejam nas opções acima
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

prompt_location_message_text = \
"""
Utilize o WhatsApp para enviar a localização de onde encontrou o problema.
Se você não souber como fazer isto, não tem problema!
Basta consultar este site aqui: https://canaltech.com.br/apps/como-enviar-sua-localizacao-pelo-whatsapp/
"""

present_reward_message_text = \
"""
Agradecemos sua denúncia. Fique com a dica de um dos nossos parceiros:\n
"""

about_text = \
"""
O bot do CycleSpot é um bot do Whatsapp que recebe as suas denúncias sobre problemas nas ciclofaixas.
No futuro, elas serão encaminhadas para a prefeitura para que eles possam melhorar tais problemas.
Envie o máximo de denúncias que você conseguir, pois assim as ruas irão ficar muito melhor para você e para outros ciclistas também!
Também, você pode receber ofertas após um certo período de tempo. Isso pode ser configurado.
Digite 1 para fazer a sua denúncia.
Digite 3 para configurar a frequência das ofertas que você pode receber periodicamente.
"""

asleep_text = \
"""
Já faz um dia desde a sua última mensagem.
Digite:
'1' para continuar.
'Sair' para cancelar a denúncia.
"""

choose_frequency = \
"""
Digite:
'1' para receber ofertas a cada 1 dia
'2' para receber ofertas a cada 2 dias
'3' para receber ofertas a cada 3 dias
'4' para receber ofertas a cada 1 semana
'5' para receber ofertas a cada 2 semanas
'6' para não receber ofertas
"""
