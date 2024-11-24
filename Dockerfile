# Usar a imagem oficial do Python
FROM python:3.9

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de dependência para o container
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . /app/

# Expor a porta em que a aplicação Flask vai rodar
EXPOSE 5000

# Definir o comando para rodar a aplicação
CMD ["python", "app.py"]
