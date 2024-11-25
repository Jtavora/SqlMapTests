import psycopg2
from flask import Flask, request, jsonify
import os
from flasgger import Swagger

app = Flask(__name__)

# Configuração do Swagger
swagger = Swagger(app)

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

@app.route('/', methods=['GET'])
def index():
    """
    Endpoint para testar a API
    ---
    responses:
      200:
        description: Retorna a mensagem de teste
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                email TEXT,
                password TEXT
            ) 
            ''')
            cursor.execute("INSERT INTO users (name, email, password) VALUES ('John Doe', 'john@example.com', 'password123')")
            cursor.execute("INSERT INTO users (name, email, password) VALUES ('Jane Smith', 'jane@example.com', 'password123')")
            conn.commit()

    return jsonify({'message': 'Hello, world!'})

@app.route('/user', methods=['GET'])
def get_user():
    """
    Endpoint para recuperar um usuário pelo ID
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Retorna o usuário encontrado
        schema:
          id: User
          properties:
            id:
              type: integer
              description: ID do usuário
            name:
              type: string
              description: Nome do usuário
            email:
              type: string
              description: E-mail do usuário
      404:
        description: Usuário não encontrado
    """
    user_id = request.args.get('id')

    # Usando o gerenciador de contexto para garantir que a conexão e o cursor sejam fechados
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM users WHERE id = {user_id}"
            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                return jsonify({'id': result[0][0], 'name': result[0][1], 'email': result[0][2]})
            else:
                return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Endpoint para recuperar todos os usuários
    ---
    responses:
      200:
        description: Lista de todos os usuários
        schema:
          type: array
          items:
            id: User
            properties:
              id:
                type: integer
                description: ID do usuário
              name:
                type: string
                description: Nome do usuário
              email:
                type: string
                description: E-mail do usuário
    """
    # Usando o gerenciador de contexto para garantir que a conexão e o cursor sejam fechados
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM users"
            cursor.execute(query)
            result = cursor.fetchall()

            users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in result]

    return jsonify(users)

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint para realizar o login
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: E-mail do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
    responses:
      200:
        description: Login bem-sucedido
        schema:
          id: User
          properties:
            id:
              type: integer
              description: ID do usuário
            name:
              type: string
              description: Nome do usuário
            email:
              type: string
              description: E-mail do usuário
      401:
        description: Credenciais inválidas
    """
    email = request.form['email']
    password = request.form['password']

    # Usando o gerenciador de contexto para garantir que a conexão e o cursor sejam fechados
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchall()

            if result:
                return jsonify({'message': 'Login successful', 'user': {'id': result[0][0], 'name': result[0][1], 'email': result[0][2]}})
            else:
                return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/create_user', methods=['POST'])
def create_user():
    """
    Endpoint para criar um novo usuário
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Nome do usuário
      - name: email
        in: formData
        type: string
        required: true
        description: E-mail do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
    responses:
      201:
        description: Usuário criado com sucesso
    """
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Usando o gerenciador de contexto para garantir que a conexão e o cursor sejam fechados
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{password}')"
            cursor.execute(query)
            conn.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/edit_user', methods=['PUT'])
def edit_user():
    """
    Endpoint para editar um usuário existente
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: ID do usuário
      - name: name
        in: formData
        type: string
        required: true
        description: Nome do usuário
      - name: email
        in: formData
        type: string
        required: true
        description: E-mail do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
    responses:
      200:
        description: Usuário atualizado com sucesso
    """
    user_id = request.args.get('id')
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Usando o gerenciador de contexto para garantir que a conexão e o cursor sejam fechados
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"UPDATE users SET name = '{name}', email = '{email}', password = '{password}' WHERE id = {user_id}"
            cursor.execute(query)
            conn.commit()

    return jsonify({'message': 'User updated successfully'})

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    """
    Endpoint para deletar um usuário
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado com sucesso
    """
    user_id = request.args.get('id')

    # Usando o gerenciador de contexto para garantir que a conexão e o cursor sejam fechados
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"DELETE FROM users WHERE id = {user_id}"
            cursor.execute(query)
            conn.commit()

    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')