import requests
import time
from app.core.config import settings

WHATSAPP_API_URL = settings.whatsapp_api_url
WHATSAPP_API_URL_SEND = settings.whatsapp_api_url_send
APIKEY = settings.apikey


def registrar_e_enviar_mensagem(phone: str, mensagem: str):
    # 1. Registrar o número
    registrar_url = WHATSAPP_API_URL
    registrar_params = {
        "apikey": APIKEY,
        "phone": phone
    }
    reg_response = requests.get(registrar_url, params=registrar_params)

    # 2. Espera um pouco para garantir o registro
    time.sleep(1)

    # 3. Enviar a mensagem
    enviar_url = WHATSAPP_API_URL_SEND
    enviar_params = {
        "apikey": APIKEY,
        "phone": phone,
        "text": mensagem
    }
    send_response = requests.get(enviar_url, params=enviar_params)

    return {
        "registro_status": reg_response.status_code,
        "registro_resposta": reg_response.text,
        "envio_status": send_response.status_code,
        "envio_resposta": send_response.text
    }

# def registrar_whatsapp(phone: str, mensagem: str):
#     url = WHATSAPP_API_URL
#     params = {
#         "apikey": APIKEY,
#         "phone": phone
#     }
#     response = requests.get(url, params=params)
#     return response.status_code, response.text


# def enviar_mensagem_whatsapp(phone: str, mensagem: str):
#     url = WHATSAPP_API_URL_SEND
#     params = {
#         "apikey": APIKEY,
#         "phone": phone,
#         "text": mensagem
#     }
#     response = requests.get(url, params=params)
#     return response.status_code, response.text
