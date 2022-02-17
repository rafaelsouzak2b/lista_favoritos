from src.app.ma import ma
from src.app.models.favoritos import FavoritoModel

class FavoritoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoritoModel
        load_instance = True
        include_fk = True
        include_relationships = True