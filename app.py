from marshmallow import ValidationError

from src.app.ma import ma
from src.app.db import db
from src.app.controllers.cliente import Cliente, ClienteList
from src.app.controllers.favoritos import FavoritoList, Favorito
from src.app.controllers.usuario import UsuarioAuth, Usuario

from src.app.server.instance import server
import logging

api = server.api
app = server.app
log = logging.getLogger(__name__)

@app.before_first_request
def create_tables():
    db.create_all()


server.cliente_ns.add_resource(ClienteList, '/clientes')
server.cliente_ns.add_resource(Cliente, '/clientes/<string:email>')
server.favoritos_ns.add_resource(FavoritoList, '/clientes/<string:email>/favoritos')
server.favoritos_ns.add_resource(Favorito, '/clientes/<string:email>/favoritos/<string:id_produto>')
server.usuario_ns.add_resource(UsuarioAuth, '/usuario/auth')
server.usuario_ns.add_resource(Usuario, '/usuario')

if __name__ == '__main__':
    log.info('API inicializada')
    db.init_app(app)
    ma.init_app(app)
    server.run()