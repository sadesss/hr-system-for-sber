import datetime

from gigachat.models import AccessToken, ChatCompletion

from GigaCredentials import GigaCredentials

from gigachat import GigaChat

giga_credentials: GigaCredentials = GigaCredentials()

if __name__ == "__main__":
    giga_credentials: GigaCredentials = GigaCredentials()
    giga: GigaChat = GigaChat(credentials=giga_credentials.get_base_encoded(), verify_ssl_certs=False)
    response: AccessToken = giga.get_token()
    response: ChatCompletion = giga.chat("Кратко: когда образовался СССР?")
    print(response.choices[0].message.content)