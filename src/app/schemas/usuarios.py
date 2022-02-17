from src.app.ma import ma
from src.app.models.usuarios import UsuarioModel

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_instance = True