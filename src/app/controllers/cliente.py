from flask import request
from flask_restx import Resource, fields
from src.app.db import db

from src.app.models.clientes import ClienteModel
from src.app.schemas.clientes import ClienteSchema
from src.app.auth import token_required

from src.app.server.instance import server
from src.app.models.erro import erro

cliente_ns = server.cliente_ns
cliente_schema = ClienteSchema()
cliente_list_schema = ClienteSchema(many=True)

CLIENTE_NAO_ENCONTRADO = 'Cliente não encontrado.'
CLIENTE_EMAIL_UTILIZADO = 'Cliente já cadastrado com esse e-mail.'

item = cliente_ns.model('Cliente', {
    'nome': fields.String(description='Nome do cliente', max_length=80, min_length=3,required=True),
    'email': fields.String(description='E-mail do cliente', max_length=250, min_length=3, required=True)
})

class Cliente(Resource):
    @cliente_ns.doc(description='Visualizar cliente')
    @cliente_ns.doc(security='apikey')
    @cliente_ns.response(200, 'OK', item)
    @cliente_ns.response(404, 'Not Found', erro)
    @cliente_ns.response(401, 'Unauthorized', erro)
    @token_required
    def get(self, email):
        cliente_data = ClienteModel.find_by_email(email)
        if cliente_data:
            return cliente_schema.dump(cliente_data), 200
        return {
            'message': CLIENTE_NAO_ENCONTRADO
        }, 404
    
    @cliente_ns.doc(description='Atualizar cliente')
    @cliente_ns.doc(security='apikey')
    @cliente_ns.expect(item, validate=True)
    @cliente_ns.response(200, 'OK', item)
    @cliente_ns.response(404, 'Not Found', erro)
    @cliente_ns.response(401, 'Unauthorized', erro)
    @token_required
    def put(self, email):
        cliente_data = getCliente(email)
        if cliente_data:
            cliente_json = request.get_json()
            cliente_data.nome = cliente_json['nome']
            cliente_data.email = cliente_json['email']
            cliente_data.save_to_db()
            return cliente_schema.dump(cliente_data), 200
        return {
            'message': CLIENTE_NAO_ENCONTRADO
        }, 404

    @cliente_ns.doc(description='Deletar cliente')
    @cliente_ns.doc(security='apikey')
    @cliente_ns.response(204, 'No Content')
    @cliente_ns.response(404, 'Not Found', erro)
    @cliente_ns.response(401, 'Unauthorized', erro)
    @token_required
    def delete(self, email):
        cliente_data = getCliente(email)
        if cliente_data:
            cliente_data.delete_from_db()
            return '', 204
        return {
            'message': CLIENTE_NAO_ENCONTRADO
        }, 404

class ClienteList(Resource):
    @cliente_ns.doc(description='Visualizar todos clientes')
    @cliente_ns.doc(security='apikey')
    @cliente_ns.response(200, 'OK', item)
    @cliente_ns.response(401, 'Unauthorized', erro)
    @token_required
    def get(self):
        return cliente_list_schema.dump(ClienteModel.find_all()), 200
    
    @cliente_ns.doc(description='Inserir cliente')
    @cliente_ns.doc(security='apikey')
    @cliente_ns.expect(item, validate=True)
    @cliente_ns.response(201, 'Created', item)
    @cliente_ns.response(400, 'Bad Request', erro)
    @cliente_ns.response(401, 'Unauthorized', erro)
    @token_required
    def post(self):
        cliente_json = request.get_json()
        cliente_data = ClienteModel.find_by_email(cliente_json['email'])
        if not cliente_data:
            cliente_data = cliente_schema.load(cliente_json, session=db.session)
            cliente_data.save_to_db()
            return cliente_schema.dump(cliente_data), 201
        return {
            'message': CLIENTE_EMAIL_UTILIZADO
        }, 400
        
def getCliente(email):
    cliente_data = ClienteModel.find_by_email(email)
    return cliente_data
        