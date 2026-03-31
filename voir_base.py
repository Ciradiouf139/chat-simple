import sqlite3
import os

def afficher_base_donnees():
    """Affiche le contenu de la base de données SQLite"""
    
    if not os.path.exists('chat.db'):
        print("❌ La base de données n'existe pas encore.")
        print("💡 Lancez d'abord l'application avec : python app.py")
        return
    
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    
    print("🗄️  BASE DE DONNÉES - CHAT SIMPLE")
    print("=" * 50)
    
    # Afficher les messages
    print("\n📨 MESSAGES :")
    cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10')
    messages = cursor.fetchall()
    
    if messages:
        for msg in messages:
            print(f"  ID: {msg[0]} | User: {msg[1]} | Message: {msg[2][:30]}... | Heure: {msg[3]}")
    else:
        print("  📭 Aucun message pour le moment")
    
    # Afficher les utilisateurs
    print("\n👥 UTILISATEURS CONNECTÉS :")
    cursor.execute('SELECT * FROM users ORDER BY joined_at DESC')
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"  ID: {user[0]} | User: {user[1]} | Couleur: {user[2]} | Connexion: {user[3]}")
    else:
        print("  🚫 Aucun utilisateur connecté")
    
    # Statistiques
    print("\n📊 STATISTIQUES :")
    cursor.execute('SELECT COUNT(*) FROM messages')
    nb_messages = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users')
    nb_users = cursor.fetchone()[0]
    
    print(f"  📨 Total messages : {nb_messages}")
    print(f"  👥 Total utilisateurs : {nb_users}")
    
    # Structure des tables
    print("\n🏗️  STRUCTURE DES TABLES :")
    
    print("\n  Table 'messages' :")
    cursor.execute('PRAGMA table_info(messages)')
    columns = cursor.fetchall()
    for col in columns:
        print(f"    - {col[1]} ({col[2]})")
    
    print("\n  Table 'users' :")
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    for col in columns:
        print(f"    - {col[1]} ({col[2]})")
    
    conn.close()
    print("\n✅ Base de données consultée avec succès !")

if __name__ == "__main__":
    afficher_base_donnees()
