from src.app.db import db
class FavoritoModel(db.Model):
    __tablename__ = 'lista_favoritos'

    email_cliente = db.Column(db.String(250), db.ForeignKey('clientes.email', ondelete='cascade'), primary_key = True)
    id_produto = db.Column(db.String(50), primary_key = True)
    favoritos = db.relationship("ClienteModel")

    def __init__(self, email_cliente, id_produto):
        self.email_cliente = email_cliente
        self.id_produto = id_produto

    def __repr__(self):
        return f'FavoritoModel(email_cliente={self.email_cliente}, id_produto={self.id_produto})'

    @classmethod
    def find_by_email(cls, email_cliente):
        return cls.query.filter_by(email_cliente=email_cliente).all()
    
    @classmethod
    def find_by_email_cliente_produto(cls, email_cliente, id_produto):
        return cls.query.filter_by(email_cliente=email_cliente, id_produto=id_produto).first()
    
    @classmethod
    def delete_lista(cls, email_cliente):
        cls.query.filter_by(email_cliente=email_cliente).delete()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
