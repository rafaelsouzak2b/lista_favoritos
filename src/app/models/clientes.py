from src.app.db import db

class ClienteModel(db.Model):
    __tablename__ = 'clientes'

    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(250), primary_key = True)

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def __repr__(self):
        return f'ClienteModel(nome={self.nome}, email={self.email})'

    def json(self):
        return {
            'nome': self.nome,
            'email': self.email
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()