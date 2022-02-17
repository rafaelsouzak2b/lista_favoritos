from flask import request
from flask_restx import Resource, fields
import requests
import json

from src.app.db import db
from src.app.models.favoritos import FavoritoModel
from src.app.models.clientes import ClienteModel
from src.app.schemas.favoritos import FavoritoSchema
from src.app.auth import token_required
from config import url_produtos

from src.app.server.instance import server
from src.app.models.erro import erro

favoritos_ns = server.favoritos_ns
favorito_schema = FavoritoSchema()
favorito_list_schema = FavoritoSchema(many=True)

CLIENTE_NAO_ENCONTRADO = 'Cliente não encontrado.'
PRODUTO_UTILIZADO = 'Produto já cadastrado com na lista de favoritos.'
PRODUTO_NAO_ASSOCIADO = 'Produto não pertence a lista de favoritos.'

produto = favoritos_ns.model('Produto', {
        'id': fields.Integer,
        'title': fields.String,
        'image': fields.String,
        'price': fields.Float,
        'reviewScore': fields.Float
    })


favorito = favoritos_ns.model('Favoritos', {
    'cliente': fields.String(description='Cliente'),
    'produtos': fields.List(fields.Nested(produto))
})

class FavoritoList(Resource):
    @favoritos_ns.doc(description='Listar produtos da lista de favoritos do cliente')
    @favoritos_ns.doc(security='apikey')
    @favoritos_ns.response(200, 'OK', favorito)
    @favoritos_ns.response(404, 'Not Found', erro)
    @favoritos_ns.response(401, 'Unauthorized', erro)
    @token_required
    def get(self, email):
        cliente_data = getCliente(email)
        if not cliente_data:
            return {
                'message': CLIENTE_NAO_ENCONTRADO
            }, 404

        favoritos_data = FavoritoModel.find_by_email(email)
        data = []
        for x in favoritos_data:
            response = requests.request("GET", f'{url_produtos}{x.id_produto}/', headers={}, data={})
            if response.status_code != 200:
               continue
            produto = json.loads(response.text)
            review = produto.get('reviewScore')
            data.append({
                'id': produto['id'],
                'title': produto['title'],
                'image': produto['image'],
                'price': produto['price'],
                'reviewScore': review
            })
        return {
            'cliente': f'{cliente_data.nome}',
            'produtos': data
        }, 200


    @favoritos_ns.doc(description='Deletar todos produtos da lista de favoritos do cliente')
    @favoritos_ns.doc(security='apikey')
    @favoritos_ns.response(204, 'No Content')
    @favoritos_ns.response(404, 'Not Found', erro)
    @favoritos_ns.response(401, 'Unauthorized', erro)
    @token_required
    def delete(self, email):
        cliente_data = getCliente(email)
        if not cliente_data:
            return {
                'message': CLIENTE_NAO_ENCONTRADO
            }, 404
        FavoritoModel.delete_lista(email)
        return '', 204
        

class Favorito(Resource):
    @favoritos_ns.doc(description='Inserir produto na lista favoritos do cliente')
    @favoritos_ns.doc(security='apikey')
    @favoritos_ns.response(201, 'Created', produto)
    @favoritos_ns.response(404, 'Not Found', erro)
    @favoritos_ns.response(400, 'Bad Request', erro)
    @favoritos_ns.response(401, 'Unauthorized', erro)
    @token_required
    def post(self, email, id_produto):
        cliente_data = getCliente(email)
        if not cliente_data:
            return {
                'message': CLIENTE_NAO_ENCONTRADO
            }, 404

        response = requests.request("GET", f'{url_produtos}{id_produto}/', headers={}, data={})
        if response.status_code != 200:
            return {
                'message': f'Produto {id_produto} não existe.'
            }, 400
        produto = json.loads(response.text)
        produto_data = FavoritoModel.find_by_email_cliente_produto(email, id_produto)
        if produto_data:
            return {
                'message': f'Produto {produto["title"]} já adicionado na lista de favoritos.'
            }, 400
        favorito_data = favorito_schema.load({
            'email_cliente': email,
            'id_produto': id_produto
        }, session=db.session)
        favorito_data.save_to_db()
        return {
            'produto': produto
        }, 201

    @favoritos_ns.doc(description='Deletar produto da lista de favoritos do cliente')
    @favoritos_ns.doc(security='apikey')
    @favoritos_ns.response(204, 'No Content')
    @favoritos_ns.response(404, 'Not Found', erro)
    @favoritos_ns.response(401, 'Unauthorized', erro)
    @token_required
    def delete(self, email, id_produto):
        cliente_data = getCliente(email)
        if not cliente_data:
            return {
                'message': CLIENTE_NAO_ENCONTRADO
            }, 404

        favorito_data = FavoritoModel.find_by_email_cliente_produto(email, id_produto)
        if favorito_data:
            favorito_data.delete_from_db()
            return '', 204
        return {
            'message': PRODUTO_NAO_ASSOCIADO
        }, 404

def getCliente(email):
    cliente_data = ClienteModel.find_by_email(email)
    return cliente_data
