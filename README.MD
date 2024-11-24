# Testes de SQL Injection com SQLMap

Este repositório contém uma API Flask vulnerável a SQL Injection para fins de teste e demonstração. O objetivo é demonstrar como o SQLMap pode ser usado para realizar ataques de injeção SQL em APIs que não utilizam práticas de segurança adequadas, como o uso de parâmetros preparados.

## Funcionalidade

A API oferece endpoints para gerenciamento de usuários, incluindo:
- Criação de usuários
- Edição de usuários
- Exclusão de usuários
- Consulta de usuários (por ID ou todos os usuários)
- Login de usuários

Esta API é vulnerável a SQL Injection em todos os endpoints que utilizam consultas SQL sem parâmetros preparados, permitindo a exploração dessa falha de segurança.

## Pré-requisitos

- Docker
- Docker Compose

## Como Rodar a Aplicação

Para rodar a aplicação, você pode usar o Docker com o `docker-compose`.

1. Clone este repositório:

   ```bash
   git clone <URL do repositório>
   cd <diretório do repositório>
   ```
2. Execute o Docker Compose para iniciar a aplicação:

   ```bash
   docker-compose up -d
   ```

### Teste 1: Testando o endpoint `GET /user?id={id}`

Execute o seguinte comando para testar a vulnerabilidade de SQL Injection no endpoint que recupera um usuário pelo ID:

 ```bash
    python3 sqlmap.py -u "http://localhost:5000/user?id=1" --dbs --risk=3 --level=5
 ```

Explicação:

- `-u "http://localhost:5000/user?id=1"`: URL do endpoint com o parâmetro `id`.
- `--dbs`: Solicita ao sqlmap que recupere o nome dos bancos de dados disponíveis.
- `--risk=3 --level=5`: Define o nível de risco e o nível de teste do sqlmap para realizar testes mais agressivos e profundos.

Este teste irá verificar se a aplicação está vulnerável a SQL Injection no parâmetro `id` e buscará detalhes do banco de dados.

### Teste 2: Testando o endpoint `POST /login`

Execute o seguinte comando para testar a vulnerabilidade de SQL Injection no endpoint de login:

 ```bash
python3 sqlmap.py -u "http://localhost:5000/login" --data "email=admin@example.com&password=' OR '1'='1" --risk=3 --level=5
 ```

Explicação:

- `-u "http://localhost:5000/login"`: URL do endpoint de login.
- `--data "email=admin@example.com&password=' OR '1'='1"`: Envia dados de login com uma injeção SQL no parâmetro `password`.
- `--risk=3 --level=5`: Configura os níveis de risco e profundidade de teste.

Este comando irá testar se é possível realizar um login bypass usando SQL Injection, explorando a falha no parâmetro `password`.

### Teste 3: Testando o endpoint `POST /create_user`

Execute o seguinte comando para testar a vulnerabilidade de SQL Injection no endpoint que cria um novo usuário:

 ```bash
python3 sqlmap.py -u "http://localhost:5000/create_user" --data "name=Test&email=test@example.com&password=' OR '1'='1" --risk=3 --level=5
 ```

Explicação:

- `-u "http://localhost:5000/create_user"`: URL do endpoint de criação de usuário.
- `--data "name=Test&email=test@example.com&password=' OR '1'='1"`: Envia dados com injeção SQL no parâmetro `password`.
- `--risk=3 --level=5`: Configura os níveis de risco e profundidade de teste.

Este teste verifica se é possível criar um novo usuário através de uma injeção SQL no parâmetro `password`.

### Teste 4: Testando o endpoint `PUT /edit_user?id={id}`

Execute o seguinte comando para testar a vulnerabilidade de SQL Injection no endpoint que edita um usuário existente:

 ```bash
python3 sqlmap.py -u "http://localhost:5000/edit_user?id=1" --data "name=UpdatedName&email=updated@example.com&password=' OR '1'='1" --risk=3 --level=5
 ```

Explicação:

- `-u "http://localhost:5000/edit_user?id=1"`: URL do endpoint de edição de usuário.
- `--data "name=UpdatedName&email=updated@example.com&password=' OR '1'='1"`: Envia dados de edição com uma injeção SQL no parâmetro `password`.
- `--risk=3 --level=5`: Configura os níveis de risco e profundidade de teste.

Este teste irá verificar se é possível alterar os dados de um usuário existente através de uma injeção SQL no parâmetro `password`.

### Teste 5: Testando o endpoint `DELETE /delete_user?id={id}`

Execute o seguinte comando para testar a vulnerabilidade de SQL Injection no endpoint que deleta um usuário:
 
 ```bash
python3 sqlmap.py -u "http://localhost:5000/delete_user?id=1" --risk=3 --level=5
 ```

Explicação:

- `-u "http://localhost:5000/delete_user?id=1"`: URL do endpoint de deletação de usuário.
- `--risk=3 --level=5`: Configura os níveis de risco e profundidade de teste.

Este teste verificará se é possível deletar um usuário utilizando uma injeção SQL no parâmetro `id`.

## Como Funciona a Aplicação

- A aplicação é um servidor Flask que expõe diversas rotas vulneráveis.
- Ela se conecta a um banco de dados PostgreSQL, que armazena informações sobre usuários.
- A vulnerabilidade de SQL Injection está presente porque as consultas SQL são formadas diretamente a partir de parâmetros fornecidos pelo usuário, sem o uso de parâmetros preparados ou ORM.

### Endpoints da API

- `GET /`: Retorna uma mensagem de teste.
- `GET /user?id={id}`: Recupera um usuário pelo ID.
- `GET /users`: Recupera todos os usuários.
- `POST /login`: Realiza o login de um usuário.
- `POST /create_user`: Cria um novo usuário.
- `PUT /edit_user?id={id}`: Edita um usuário existente.
- `DELETE /delete_user?id={id}`: Deleta um usuário.

## Conclusão

Este projeto serve como uma demonstração de como vulnerabilidades de SQL Injection podem ser exploradas em uma aplicação web. Utilize o `sqlmap` para testar cada uma das rotas e explorar as falhas de segurança da API.