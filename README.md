## MVP - MAC0467 - Empreendedorismo Digital
---
# Cycle
#### Chatbot para denúncia de ciclovias


## Ambiente de Desenvolvimento

### Gerenciamento de Dependências

Este projeto usa `pyenv` e `poetry` para o gerenciamento e manutenção das dependêcias.

Depois de instalar os dois utilitários, ainda é necessário instalar a versão 3.11.3 do python.

Para subir o ambiente de desenvolvimento ou produção, é necessário ativar o ambiente virtual e as dependências do projeto utilizando:

```[bash]
$ pyenv shell 3.11.3
$ poetry shell
```

### Subindo o Servidor

Antes de rodar, devemos criar o banco de dados:
```[bash]
$ python manage.py migrate
``` 

Para subir o servidor de produção, basta executar o comando:
```[bash]
$ python manage.py runserver
``` 

Além disso, é necessário expor a porta local do servidor às chamadas do Twilio, o faça usando o ngrok:

```[bash]
$ ngrok http 8000
``` 

Entre a saída do comando, identifique o endereço IP para encaminhamento (forwarding) das requests, o atualize entre os `ALLOWED_HOSTS` de `settings.py`, e o adicione como listenign point dentro do console do Twilio (Sandbox settings -> When a message comes in), adicionando ao final `/bot/msgin`

Não se esqueça de preencher o .env com as credenciais do Twilio ( `TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN`), utilizando as `Live credentials`.

### Contatando o Chatbot

Envie a mensagem
```
join <nome-do-chat> 
```
para +1 415 523 8886