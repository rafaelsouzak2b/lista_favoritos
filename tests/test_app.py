import base64
import string
import random
import json

random_str = string.ascii_letters
from src.app.models.usuarios import UsuarioModel
username = ''.join(random.choice(random_str) for i in range(10))
password = 'teste'
nome_cliente = ''.join(random.choice(random_str) for i in range(10))
email_cliente = ''.join(random.choice(random_str) for i in range(20))

token = ''

def test_inserir_usuario_201(client):
    '''
    Teste de inserção de usuario
    '''
    payload = {
    'username': username,
    'password': password
    }
    response = client.post('/api/usuario', json=payload)

    retorno = json.loads(response.data)
    
    assert response.status_code == 201
    assert len(retorno) > 0

def test_inserir_usuario_ja_cadastrado_400(client):
    '''
    Teste de inserção de usuario ja existente
    '''
    payload = {
    'username': username,
    'password': password
    }
    response = client.post('/api/usuario', json=payload)
    
    assert response.status_code == 400

def test_inserir_usuario_400(client):
    '''
    Teste de inserção de usuario sem payload
    '''
    response = client.post('/api/usuario')
    
    assert response.status_code == 400

def test_autenticar_usuario_200(client):
    '''
    Teste de geração de token
    '''
    userpass = f'{username}:{password}'
    base64_val = base64.b64encode(userpass.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {base64_val}'
    }

    response = client.post('/api/usuario/auth', headers=headers)

    global token
    
    retorno = json.loads(response.data)

    token = retorno['token']

    usuario_data = UsuarioModel.find_by_username(username)
    if usuario_data:
        usuario_data.delete_from_db()

    assert response.status_code == 200
    assert len(retorno) > 0

def test_inserir_clientes_201(client):
    '''
    Teste de inserção de cliente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
    'nome': nome_cliente,
    'email': email_cliente
    }

    response = client.post('/api/clientes', headers=headers, json=payload)
    
    retorno = json.loads(response.data)

    assert response.status_code == 201
    assert len(retorno) > 0

def test_inserir_clientes_ja_cadastrado_400(client):
    '''
    Teste de inserção de cliente ja cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
    'nome': nome_cliente,
    'email': email_cliente
    }

    response = client.post('/api/clientes', headers=headers, json=payload)
    assert response.status_code == 400

def test_inserir_clientes_400(client):
    '''
    Teste de inserção de cliente sem payload
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.post('/api/clientes', headers=headers)
    assert response.status_code == 400

def test_visualizar_todos_clientes_200(client):
    '''
    Teste de visualização de todos os clientes
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.get('/api/clientes', headers=headers)
    retorno = json.loads(response.data)

    assert response.status_code == 200
    assert len(retorno) > 0

def test_visualizar_clientes_200(client):
    '''
    Teste de visualização de cliente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.get(f'/api/clientes/{email_cliente}', headers=headers)
    
    retorno = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(retorno) > 0

def test_visualizar_clientes_404(client):
    '''
    Teste de visualização de cliente não cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = client.get(f'/api/clientes/{email_cliente}k', headers=headers)
    
    assert response.status_code == 404

def test_alterar_clientes_200(client):
    '''
    Teste de atualização de cliente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
    'nome': nome_cliente,
    'email': email_cliente
    }

    response = client.put(f'/api/clientes/{email_cliente}', headers=headers, json=payload)

    retorno = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(retorno) > 0

def test_alterar_clientes_404(client):
    '''
    Teste de atualização de cliente não cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
    'nome': nome_cliente,
    'email': email_cliente
    }

    response = client.put(f'/api/clientes/{email_cliente}k', headers=headers, json=payload)
    
    assert response.status_code == 404

def test_alterar_clientes_400(client):
    '''
    Teste de atualização de cliente sem payload
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.put(f'/api/clientes/{email_cliente}', headers=headers)
    
    assert response.status_code == 400

def test_deletar_clientes_404(client):
    '''
    Teste de deletar cliente não cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.delete(f'/api/clientes/{email_cliente}k', headers=headers)
    
    assert response.status_code == 404

def test_visualizar_lista_favoritos_200(client):
    '''
    Teste de visualização da lista de favoritos
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.get(f'/api/clientes/{email_cliente}/favoritos', headers=headers)

    retorno = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(retorno) > 0


def test_visualizar_lista_favoritos_404(client):
    '''
    Teste de visualização da lista de favoritos de cliente não cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.get(f'/api/clientes/{email_cliente}k/favoritos', headers=headers)
    
    assert response.status_code == 404


def test_inserir_lista_favoritos_201(client):
    '''
    Teste de inclusao de produto na lista de favoritos
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.post(f'/api/clientes/{email_cliente}/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)

    retorno = json.loads(response.data)
    
    assert response.status_code == 201
    assert len(retorno) > 0

def test_inserir_lista_favoritos_400(client):
    '''
    Teste de inclusão de produto ja inserido na lista de favoritos
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.post(f'/api/clientes/{email_cliente}/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)
    
    assert response.status_code == 400

def test_inserir_lista_favoritos_produto_nao_existe_400(client):
    '''
    Teste de inclusão de produto não existente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.post(f'/api/clientes/{email_cliente}/favoritos/teste', headers=headers)
    
    assert response.status_code == 400

def test_inserir_lista_favoritos_404(client):
    '''
    Teste de inclusão de produto na lista de favoritos de cliente que não existe
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.post(f'/api/clientes/{email_cliente}k/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)
    
    assert response.status_code == 404

def test_deletar_lista_favoritos_204(client):
    '''
    Teste de exclusão do produto na lista de favoritos
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.delete(f'/api/clientes/{email_cliente}/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)
    
    assert response.status_code == 204

def test_deletar_lista_favoritos_404(client):
    '''
    Teste de exclusão do produto na lista de favoritos de produto que não esta na lista do cliente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.delete(f'/api/clientes/{email_cliente}/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)
    
    assert response.status_code == 404

def test_deletar_lista_favoritos_cliente_nao_cadastrado_404(client):
    '''
    Teste de exclusão do produto na lista de favoritos de cliente que não esta cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.delete(f'/api/clientes/{email_cliente}k/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)
    
    assert response.status_code == 404


def test_deletar_toda_lista_favoritos_204(client):
    '''
    Teste de exclusão de toda lista de favoritos do cliente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }

    client.post(f'/api/clientes/{email_cliente}/favoritos/1bf0f365-fbdd-4e21-9786-da459d78dd1f', headers=headers)
   
    response = client.delete(f'/api/clientes/{email_cliente}/favoritos', headers=headers)
    
    assert response.status_code == 204

def test_deletar_toda_lista_favoritos_404(client):
    '''
    Teste de exclusão de toda lista de favoritos de cliente não cadastrado
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.delete(f'/api/clientes/{email_cliente}f/favoritos', headers=headers)
    
    assert response.status_code == 404

def test_deletar_clientes_204(client):
    '''
    Teste exclusão de cliente
    '''
    headers = {
        'Authorization': f'Bearer {token}'
    }
   
    response = client.delete(f'/api/clientes/{email_cliente}', headers=headers)
    
    assert response.status_code == 204













