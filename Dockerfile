# Dockerfile para FastAPI + Uvicorn
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Copia o código
COPY . .

# Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta padrão do Uvicorn
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
