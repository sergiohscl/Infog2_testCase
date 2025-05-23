from app.services.whatsapp import enviar_mensagem_whatsapp


def notificar_novo_pedido(nome_cliente: str, telefone: str):
    mensagem = f"Olá {nome_cliente}, seu pedido foi recebido com sucesso!"
    status, resposta = enviar_mensagem_whatsapp(telefone, mensagem)
    return status, resposta
