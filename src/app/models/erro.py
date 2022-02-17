from flask_restx import fields
from src.app.server.instance import server

erro = server.api.model('Erro', {
    'message': fields.String(description='Mensagem de erro')
})