from src.app.ma import ma
from src.app.models.clientes import ClienteModel

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClienteModel
        load_instance = True