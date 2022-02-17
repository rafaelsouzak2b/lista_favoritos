#Teste segurança de autenticação de usuario
def test_Unauthorized_usuario(client):
    response = client.post('/api/usuario/auth')
    
    assert response.status_code == 401

#Teste segurança de autenticação de cliente
def test_Unauthorized_inserir_cliente(client):
    payload = {
    'email': 'teste',
    'nome': 'teste'
    }

    response = client.post('/api/clientes', json=payload)
    
    assert response.status_code == 401

def test_Unauthorized_visualizar_todos_cliente(client):

    response = client.get('/api/clientes')
    
    assert response.status_code == 401

def test_Unauthorized_visualizar_cliente(client):

    response = client.get('/api/clientes/teste')
    
    assert response.status_code == 401

def test_Unauthorized_atualizar_cliente(client):
    payload = {
    'email': 'teste',
    'nome': 'teste'
    }

    response = client.put('/api/clientes/teste', json=payload)
    
    assert response.status_code == 401

def test_Unauthorized_deletar_cliente(client):

    response = client.delete('/api/clientes/teste')
    
    assert response.status_code == 401

#Teste segurança de autenticação de lista favoritos
def test_Unauthorized_visualizar_lista_favorito(client):

    response = client.get('/api/clientes/teste/favoritos')
    
    assert response.status_code == 401

def test_Unauthorized_deletar_lista_favorito(client):

    response = client.delete('/api/clientes/teste/favoritos')
    
    assert response.status_code == 401

def test_Unauthorized_insert_prod_lista_favorito(client):

    response = client.post('/api/clientes/teste/favoritos/teste')
    
    assert response.status_code == 401

def test_Unauthorized_deletar_prod_lista_favorito(client):

    response = client.delete('/api/clientes/teste/favoritos/teste')
    
    assert response.status_code == 401