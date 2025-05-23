# Teste de Codificação de Desenvolvedor Back-End

## 📄 Descrição do Problema

A especificação completa do problema está no arquivo:

**`Teste_de_Codificacao_Desenvolvedor_Backend.pdf`**

---

## ⚙️ Instalando o Ambiente Virtual

1. Crie o ambiente virtual:

```bash
python -m venv venv
```

2. Ative o ambiente virtual:

- No **Linux/macOS**:

```bash
source venv/bin/activate
```

- No **Windows**:

```bash
venv\Scripts\activate
```

---

## 📦 Instalando as Dependências do Projeto

Após ativar o ambiente virtual, instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Criando o Arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Chave secreta para JWT
secret_key=sua_chave_secreta

# Algoritmo JWT
algorithm=HS256

# Tempo de expiração do token em minutos (24 horas)
access_token_expire_minutes=1440

# URL do banco de dados PostgreSQL
database_url=postgresql://postgres:sua_senha@localhost:5432/seu_database

# Ambiente (development, production, etc.)
environment=development

# URL para registrar número no TextMeBot
whatsapp_api_url=https://api.textmebot.com/addphone.php

# URL para enviar mensagens no TextMeBot
whatsapp_api_url_send=https://api.textmebot.com/send.php

# Sua APIKey do TextMeBot
apikey=sua_chave
```

---

## 🔗 Links úteis do TextMeBot

- 💲 **Planos e preços**:  
  [https://textmebot.com/#prices](https://textmebot.com/#prices)

- 🔌 **Conectar seu número à API**:  
  [https://api.textmebot.com/status.php?apikey=apikey](https://api.textmebot.com/status.php?apikey=apikey)

> **Atenção**: Substitua `apikey` pela sua chave real na URL acima para verificar o status de conexão com o WhatsApp.

---

## 🚀 Executando o Projeto

Após configurar tudo, inicie a API com o Uvicorn:

```bash
uvicorn app.main:app --reload
```

A aplicação será executada com swagger em [http://localhost:8000/docs](http://localhost:8000/docs)


