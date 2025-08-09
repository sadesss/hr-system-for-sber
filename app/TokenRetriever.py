import datetime

from gigachat.models import AccessToken, ChatCompletion

from GigaCredentials import GigaCredentials

from gigachat import GigaChat

giga_credentials: GigaCredentials = GigaCredentials()

# class TokenRetriever:
#     temp_token: bytes
#     token_expiry: datetime
#
#     # https://developers.sber.ru/docs/ru/gigachat/api/reference/rest/post-token
#     def update_token(self):
#         new_uuid: uuid.UUID = uuid.uuid4()
#         headers: dict[str, str] = {
#             'RwUID': new_uuid,
#             'Authorization': 'Basic ' + giga_credentials.get_base_encoded()
#         }
#         body = {
#             'scope': 'GIGACHAT_API_PERS'
#         }
#         response: Response = requests.post('https://ngw.devices.sberbank.ru:9443/api/v2', headers=headers, data=body, auth=())
#         self.token_expiry = datetime.datetime.fromtimestamp(response.timestamp)
#
#     def get_token(self) -> bytes:
#         return self.temp_token
#
# class TokenRetriever:
#     temp_token: bytes
#     token_expiry: datetime
#
#     def __init__(self, temp_token: bytes, token_expiry: datetime):
#         self.temp_token = response.temp_token
#         self.token_expiry = datetime.datetime.fromtimestamp(response.token_expiry)

if __name__ == "__main__":
    giga_credentials: GigaCredentials = GigaCredentials()
    giga: GigaChat = GigaChat(credentials=giga_credentials.get_base_encoded(), verify_ssl_certs=False)
    response: AccessToken = giga.get_token()
    response: ChatCompletion = giga.chat("Кратко: когда образовался СССР?")
    print(response.choices[0].message.content)