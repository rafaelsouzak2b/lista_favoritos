import pytest
@pytest.fixture(scope='session')
def client():
    flask_app = create_app('testing')

    testing_client = flask_app.test_client()
   
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client 
    ctx.pop()

def create_app(config_name):
    from app import app
    from src.app.db import db
    from src.app.ma import ma
   
    db.init_app(app)
    ma.init_app(app)

    return app
