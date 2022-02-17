import random
import string
random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(12))

url_produtos = 'http://challenge-api.luizalabs.com/api/product/'
SQLALCHEMY_DATABASE_URI = 'mysql://root:WgAe12@db/produtosfavoritos'
secret_key = key