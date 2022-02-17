from flask import request
from flask_restx import Resource, fields
from werkzeug.security import generate_password_hash

from src.app.server.instance import server
from src.app.auth import basic_auth, auth
from src.app.models.usuarios import UsuarioModel
from src.app.schemas.usuarios import UsuarioSchema
from src.app.models.erro import erro

usuario_schema= UsuarioSchema()

usuario_ns = server.usuario_ns

usuario = usuario_ns.model('Usuário', {
    'username': fields.String(description='Username do usuário', max_length=20, min_length=3,required=True),
    'password': fields.String(description='Senha do usuário', max_length=200, min_length=3,required=True)
})

token = usuario_ns.model('Token', {
  'exp': fields.String,
  'message': fields.String,
  'token': fields.String,
})

class UsuarioAuth(Resource):
    @usuario_ns.doc(description='Autenticar usuário')
    @usuario_ns.doc(security='basicAuth')
    @usuario_ns.response(200, 'OK', token)
    @usuario_ns.response(401, 'Unauthorized')
    @basic_auth.login_required
    def post(self):
        return auth()
        
class Usuario(Resource):
    @usuario_ns.doc(description='Inserir novo usuário')
    @usuario_ns.expect(usuario, validate=True)
    @usuario_ns.response(201, 'Created', usuario)
    @usuario_ns.response(400, 'Bad Request', erro)
    def post(Resource):
        usuario_json = request.get_json()
        usuario_data = UsuarioModel.find_by_username(usuario_json['username'])
        if usuario_data:
            return {
            'message': 'Usuário ja cadastrado.'
        }, 400
        usuario_json['password'] = generate_password_hash(usuario_json['password'])
        usuario_data = usuario_schema.load(usuario_json)
        usuario_data.save_to_db()
        return usuario_schema.dump(usuario_data), 201
