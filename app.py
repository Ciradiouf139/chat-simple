from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'chat_secret_key_123'

def get_db_connection():
    return sqlite3.connect('chat.db')

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        room TEXT DEFAULT 'general'
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        color TEXT DEFAULT '#000000',
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50')
    messages = cursor.fetchall()
    cursor.execute('SELECT * FROM users ORDER BY joined_at DESC')
    users = cursor.fetchall()
    conn.close()
    return render_template('chat_new.html', messages=messages, users=users)

@app.route('/login', methods=['POST'])
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
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'error': 'Non connecte'}), 401
    
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
    
    return jsonify({'success': True})

@app.route('/get_messages')
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
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, color FROM users ORDER BY joined_at DESC')
    users = cursor.fetchall()
    conn.close()
    
    users_list = []
    for user in users:
        users_list.append({
            'username': user[0],
            'color': user[1]
        })
    
    return jsonify(users_list)

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'instance': os.environ.get('INSTANCE_NAME', 'default')
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
