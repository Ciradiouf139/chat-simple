import pytest
import json
import sqlite3
import os
from app_ameliore import app, init_db, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test_chat.db'
    
    with app.test_client() as client:
        with app.app_context():
            # Initialiser la base de données de test
            if os.path.exists('test_chat.db'):
                os.remove('test_chat.db')
            init_db()
        yield client
    
    # Nettoyer
    if os.path.exists('test_chat.db'):
        os.remove('test_chat.db')

@pytest.fixture
def session(client):
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'
        sess['color'] = '#FF0000'

def test_index_redirect(client):
    """Test que la page principale redirige vers login si non connecté"""
    response = client.get('/')
    assert response.status_code == 302

def test_login_success(client):
    """Test connexion réussie"""
    response = client.post('/login', data={'username': 'testuser'})
    assert response.status_code == 302
    
    with client.session_transaction() as sess:
        assert sess['username'] == 'testuser'

def test_login_invalid(client):
    """Test connexion avec nom invalide"""
    response = client.post('/login', data={'username': 'a'})
    assert response.status_code == 200
    assert b'Nom d\'utilisateur invalide' in response.data

def test_logout(client, session):
    """Test déconnexion"""
    response = client.get('/logout')
    assert response.status_code == 302

def test_api_messages_get(client, session):
    """Test API GET messages"""
    response = client.get('/api/messages')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_api_messages_post(client, session):
    """Test API POST message"""
    response = client.post('/api/messages', 
                          json={'message': 'Hello world', 'room': 'general'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True

def test_api_messages_post_unauthorized(client):
    """Test API POST message non connecté"""
    response = client.post('/api/messages', 
                          json={'message': 'Hello world', 'room': 'general'})
    assert response.status_code == 401

def test_api_users_get(client, session):
    """Test API GET users"""
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_api_rooms_get(client, session):
    """Test API GET rooms"""
    response = client.get('/api/rooms')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 4  # 4 salons par défaut

def test_api_rooms_post(client, session):
    """Test API POST room"""
    response = client.post('/api/rooms', 
                          json={'name': 'test_room', 'description': 'Test room'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['name'] == 'test_room'

def test_api_stats(client, session):
    """Test API stats"""
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_messages' in data
    assert 'total_users' in data
    assert 'online_users' in data
    assert 'total_rooms' in data

def test_api_status(client):
    """Test API status"""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'online'
    assert 'version' in data
    assert 'features' in data

def test_metrics_endpoint(client):
    """Test endpoint Prometheus metrics"""
    response = client.get('/metrics')
    assert response.status_code == 200

def test_database_operations(client, session):
    """Test opérations base de données"""
    # Envoyer un message
    response = client.post('/api/messages', 
                          json={'message': 'Test message', 'room': 'general'})
    assert response.status_code == 200
    
    # Vérifier que le message est dans la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM messages WHERE message = ?', ('Test message',))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    assert result[0] == 'Test message'

def test_react_message_api(client, session):
    """Test API réactions"""
    # D'abord créer un message
    response = client.post('/api/messages', 
                          json={'message': 'Message for reaction', 'room': 'general'})
    assert response.status_code == 200
    
    # Ajouter une réaction (simuler message_id = 1)
    response = client.post('/api/reactions', 
                          json={'message_id': 1, 'reaction': '👍'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
