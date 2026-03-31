from flask import Flask, render_template, request, jsonify, session, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import sqlite3
import random
from datetime import datetime
import os
import json
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps
import redis

app = Flask(__name__)
app.secret_key = 'chat_secret_key_123'
socketio = SocketIO(app, cors_allowed_origins="*")

# Redis pour le cache
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
except:
    redis_client = None

# Métriques Prometheus
MESSAGES_SENT = Counter('messages_sent_total', 'Total messages sent')
MESSAGE_LATENCY = Histogram('message_latency_seconds', 'Message latency')
USERS_ONLINE = Gauge('users_online_total', 'Users currently online')
HTTP_REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])

def get_db_connection():
    return sqlite3.connect('chat.db')

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        room TEXT DEFAULT 'general'
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        color TEXT DEFAULT '#000000',
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_online INTEGER DEFAULT 1
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        reaction TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insérer les salons par défaut
    cursor.execute('''INSERT OR IGNORE INTO rooms (name, description, created_by) VALUES 
        ('general', 'Chat général pour tous', 'system'),
        ('tech', 'Discussions techniques', 'system'),
        ('random', 'Sujets aléatoires', 'system'),
        ('support', 'Aide et support', 'system')
    ''')
    
    conn.commit()
    conn.close()

def track_requests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        latency = time.time() - start_time
        HTTP_REQUESTS.labels(method=request.method, endpoint=request.endpoint, status='200').inc()
        MESSAGE_LATENCY.observe(latency)
        return response
    return decorated_function

def update_user_online_status(username, is_online=True):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE users SET is_online = ?, last_seen = CURRENT_TIMESTAMP 
                     WHERE username = ?''', (1 if is_online else 0, username))
    conn.commit()
    conn.close()
    
    # Mettre à jour Redis
    if redis_client:
        if is_online:
            redis_client.sadd('online_users', username)
            redis_client.expire('online_users', 300)  # 5 minutes
        else:
            redis_client.srem('online_users', username)
    
    # Mettre à jour la métrique
    if redis_client:
        online_count = redis_client.scard('online_users')
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_online = 1')
        online_count = cursor.fetchone()[0]
        conn.close()
    
    USERS_ONLINE.set(online_count)

# Routes principales
@app.route('/')
@track_requests
def index():
    if 'username' not in session:
        return render_template('login.html')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50')
    messages = cursor.fetchall()
    cursor.execute('SELECT * FROM users WHERE is_online = 1 ORDER BY joined_at DESC')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM rooms ORDER BY name')
    rooms = cursor.fetchall()
    conn.close()
    return render_template('chat_new.html', messages=messages, users=users, rooms=rooms)

@app.route('/login', methods=['POST'])
@track_requests
def login():
    username = request.form.get('username', '').strip()
    
    if not username or len(username) < 2:
        return render_template('login.html', error='Nom d\'utilisateur invalide')
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    user_color = random.choice(colors)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, color) VALUES (?, ?)', (username, user_color))
        conn.commit()
    except sqlite3.IntegrityError:
        cursor.execute('SELECT color FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        user_color = result[0] if result else user_color
    conn.close()
    
    session['username'] = username
    session['color'] = user_color
    
    update_user_online_status(username, True)
    
    return redirect('/')

@app.route('/logout')
@track_requests
def logout():
    if 'username' in session:
        update_user_online_status(session['username'], False)
        socketio.emit('user_left', {'username': session['username']}, room='general')
    session.clear()
    return redirect('/')

# API REST
@app.route('/api/messages', methods=['GET'])
@track_requests
def api_get_messages():
    room = request.args.get('room', 'general')
    limit = request.args.get('limit', 50, type=int)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE room = ? ORDER BY timestamp DESC LIMIT ?', (room, limit))
    messages = cursor.fetchall()
    conn.close()
    
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg[0],
            'username': msg[1],
            'message': msg[2],
            'timestamp': msg[3],
            'room': msg[4]
        })
    
    return jsonify(messages_list)

@app.route('/api/messages', methods=['POST'])
@track_requests
def api_send_message():
    if 'username' not in session:
        return jsonify({'error': 'Non connecté'}), 401
    
    data = request.json
    message = data.get('message', '').strip()
    room = data.get('room', 'general')
    
    if not message:
        return jsonify({'error': 'Message vide'}), 400
    
    username = session['username']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (username, message, room) VALUES (?, ?, ?)', (username, message, room))
    conn.commit()
    conn.close()
    
    MESSAGES_SENT.inc()
    
    # Émettre via WebSocket
    socketio.emit('new_message', {
        'username': username,
        'message': message,
        'room': room,
        'timestamp': datetime.now().isoformat()
    }, room=room)
    
    return jsonify({'success': True})

@app.route('/api/users', methods=['GET'])
@track_requests
def api_get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, color, is_online FROM users ORDER BY joined_at DESC')
    users = cursor.fetchall()
    conn.close()
    
    users_list = []
    for user in users:
        users_list.append({
            'username': user[0],
            'color': user[1],
            'is_online': bool(user[2])
        })
    
    return jsonify(users_list)

@app.route('/api/rooms', methods=['GET'])
@track_requests
def api_get_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms ORDER BY name')
    rooms = cursor.fetchall()
    conn.close()
    
    rooms_list = []
    for room in rooms:
        rooms_list.append({
            'id': room[0],
            'name': room[1],
            'description': room[2],
            'created_at': room[3],
            'created_by': room[4]
        })
    
    return jsonify(rooms_list)

@app.route('/api/rooms', methods=['POST'])
@track_requests
def api_create_room():
    if 'username' not in session:
        return jsonify({'error': 'Non connecté'}), 401
    
    data = request.json
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({'error': 'Nom du salon requis'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO rooms (name, description, created_by) VALUES (?, ?, ?)', 
                      (name, description, session['username']))
        conn.commit()
        room_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'room_id': room_id,
            'name': name,
            'description': description
        })
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Ce salon existe déjà'}), 400

@app.route('/api/stats', methods=['GET'])
@track_requests
def api_get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Statistiques des messages
    cursor.execute('SELECT COUNT(*) FROM messages')
    total_messages = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM messages WHERE timestamp >= datetime("now", "-1 day")')
    messages_today = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_online = 1')
    online_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM rooms')
    total_rooms = cursor.fetchone()[0]
    
    # Top utilisateurs
    cursor.execute('SELECT username, COUNT(*) as count FROM messages GROUP BY username ORDER BY count DESC LIMIT 5')
    top_users = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_messages': total_messages,
        'messages_today': messages_today,
        'total_users': total_users,
        'online_users': online_users,
        'total_rooms': total_rooms,
        'top_users': [{'username': user[0], 'message_count': user[1]} for user in top_users],
        'prometheus_metrics': {
            'messages_sent_total': MESSAGES_SENT._value.get(),
            'users_online_total': USERS_ONLINE._value.get()
        }
    })

@app.route('/api/reactions', methods=['POST'])
@track_requests
def api_add_reaction():
    if 'username' not in session:
        return jsonify({'error': 'Non connecté'}), 401
    
    data = request.json
    message_id = data.get('message_id')
    reaction = data.get('reaction')
    
    if not message_id or not reaction:
        return jsonify({'error': 'Données incomplètes'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reactions (message_id, username, reaction) VALUES (?, ?, ?)', 
                  (message_id, session['username'], reaction))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/metrics')
def metrics():
    return generate_latest()

# Routes legacy pour compatibilité
@app.route('/send_message', methods=['POST'])
@track_requests
def send_message():
    return api_send_message()

@app.route('/get_messages')
@track_requests
def get_messages():
    last_id = request.args.get('last_id', 0, type=int)
    room = request.args.get('room', 'general')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE id > ? AND room = ? ORDER BY timestamp ASC', (last_id, room))
    messages = cursor.fetchall()
    conn.close()
    
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg[0],
            'username': msg[1],
            'message': msg[2],
            'timestamp': msg[3],
            'room': msg[4]
        })
    
    return jsonify(messages_list)

@app.route('/get_users')
@track_requests
def get_users():
    return api_get_users()

@app.route('/api/status')
@track_requests
def api_status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'instance': os.environ.get('INSTANCE_NAME', 'default'),
        'version': '2.0.0',
        'features': {
            'websocket': True,
            'api_rest': True,
            'monitoring': True,
            'redis_cache': redis_client is not None
        }
    })

# Événements WebSocket
@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        join_room('general')
        emit('user_joined', {'username': session['username']}, room='general')

@socketio.on('disconnect')
def handle_disconnect():
    if 'username' in session:
        leave_room('general')
        update_user_online_status(session['username'], False)
        emit('user_left', {'username': session['username']}, room='general')

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room', 'general')
    if 'username' in session:
        join_room(room)
        emit('room_joined', {'username': session['username'], 'room': room}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data.get('room', 'general')
    if 'username' in session:
        leave_room(room)
        emit('room_left', {'username': session['username'], 'room': room}, room=room)

@socketio.on('typing')
def handle_typing(data):
    room = data.get('room', 'general')
    if 'username' in session:
        emit('user_typing', {'username': session['username'], 'room': room}, room=room)

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
