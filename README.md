# API Rest lista de produtos favoritos de clientes

# Recursos utilizados

- API: Flask, SQLAlchemy, MySQL
- Teste: PyTest

## Começando
Para execução do projeto será necessário a instalação do [Docker Desktop](https://www.docker.com/get-started).

Para iniciar o projeto basta clonar o projeto do GitHub num diretório de sua preferência:
 
 `git clone https://github.com/rafaelsouzak2b/lista_favoritos.git`
 
 `cd lista_favoritos`

  ## Inicialização

Após o Docker Desktop instalado e o projeto clonado, será necessário criar a imagem e o container do banco mysql.

`docker run --name mysql_container -p 3306:3306 -p 33060:33060 -e MYSQL_ROOT_HOST="%" -e MYSQL_ROOT_PASSWORD="WgAe12" -d mysql/mysql-server:latest`

Criar banco de dados no banco mysql do container mysql_container

`docker exec -i mysql_container mysql -uroot -pWgAe12 < script.sql`

Para rodar a api pode ser feito de duas maneiras executando via container no docker ou via cmd com o python instalado na maquina

 Rodando por container:
- Gerar imagem da api e iniciar o container

`docker build -t api-favoritos-image -f .\Dockerfile .
docker run --name api-favoritos --link mysql_container:db -p 5000:5000 -d api-favoritos-image`

Com o container api-favoritos rodando a api já pode ser acessada em http://localhost:5000/api

 - Rodando pelo cmd:
Para rodar a aplicação via cmd é necessário mudar a conecxão do banco de dados no arquivo `config.py`

De `SQLALCHEMY_DATABASE_URI = 'mysql://root:WgAe12@db/produtosfavoritos'` 
Para `SQLALCHEMY_DATABASE_URI = 'mysql://root:WgAe12@localhost/produtosfavoritos'`

Com o python instalado na maquina

Criar o ambiente virtual da aplicação:

`python -m venv .venv`

Ativar o ambiente virtual

`.venv\Scripts\activate.bat`

Instalar pacotes usados na aplicação

`pip install -r requirements.txt`

Rodando a api

`python app.py`

Com api rodando a api já pode ser acessada em http://localhost:5000/api

## Documentação
A documentação da api esta disponivel http://localhost:5000/api utilizando swagger

## Premissas para utilizar a api
Para utilizar a api é necessario ter um usuario cadastrado usando o endpoint POST /usuario, na documentação da api tem o modelo da requisição
Apos ter criado o usuário, é necessario gerar um token de acesso tipo Bearer para ter acesso aos demais endpoints da api. A autenticação pode ser feita pelo endipoint /usuario/auth e na requisição via Basic Authorization passar o usuário e senha criado anteriormente, na documentação também tem o modelo da requisição.

## Testes na API

Para a api rodando em container(docker)

`docker exec -i api-favoritos pytest`

Para a api rodando pelo cmd

`pytest`
