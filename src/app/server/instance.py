from flask import Flask, Blueprint
from flask_restx import Api
from flask_httpauth import HTTPBasicAuth
from config import SQLALCHEMY_DATABASE_URI
import logging

class Server():
    def __init__(self):
        self.authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Autenticação Bearer'
    },
    "basicAuth" : {
        "type" : "basic"
    }
}

        self.app = Flask(__name__)
        self.basic_auth = HTTPBasicAuth()
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.blueprint, doc='/', title='API Produtos Favoritos', authorizations=self.authorizations)
        self.app.register_blueprint(self.blueprint)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        filename='./logs/api.log',
        filemode='w'
        )

        self.cliente_ns = self.cliente_ns()
        self.favoritos_ns = self.favoritos_ns()
        self.usuario_ns = self.usuario_ns()
        

    def cliente_ns(self):
        return self.api.namespace(name='Clientes', description='Gerenciamento de clientes', path='/')
    def favoritos_ns(self):
        return self.api.namespace(name='Produtos Favoritos', description='Lista de produtos favoritos', path='/')
    def usuario_ns(self):
        return self.api.namespace(name='Usuário', description='Cadastro de usuário e autenticação', path='/')

    def run(self):
        self.app.run(
            port=5000,
            debug=False,
            host='0.0.0.0'
        )
        

server = Server()