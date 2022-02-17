from src.app.server.instance import server
from config import secret_key
from flask import request, jsonify
import jwt
import datetime
from functools import wraps
from src.app.models.usuarios import UsuarioModel
from werkzeug.security import check_password_hash

basic_auth = server.basic_auth

@basic_auth.verify_password
def authenticate(username, password):
    usuario = UsuarioModel.find_by_username(username)
    if username and password:
        if usuario and check_password_hash(usuario.password, password):
            return True
        else:
            return False
    return False

def auth():
    auth = request.authorization
    token = jwt.encode({'username': auth.username, 'exp': datetime.datetime.now() + datetime.timedelta(hours=4) },
                        secret_key, algorithm="HS256")
    return jsonify({'message': 'Validação bem sucedida.', 'token': token,
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=4)})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return {'message': 'Token não informado.'}, 401
        
        if not 'Bearer' in token and not 'bearer' in token:
            return {'message': 'Token inválido.'}, 401

        token = token.replace('Bearer ', '').replace('bearer ', '')
        try:
            jwt.decode(token, secret_key, algorithms="HS256")
        except:
            return {'message': 'Token inválido ou expirado.'}, 401
        return f(*args, **kwargs)
    return decorated