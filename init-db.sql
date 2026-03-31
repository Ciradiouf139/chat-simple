-- Script d'initialisation pour PostgreSQL
-- Création des tables pour la base de données de chat

-- Table des messages
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    room VARCHAR(50) DEFAULT 'general'
);

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#000000',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_online BOOLEAN DEFAULT TRUE
);

-- Table des salons
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50)
);

-- Table des réactions
CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL,
    username VARCHAR(50) NOT NULL,
    reaction VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
);

-- Index pour optimiser les performances
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room);
CREATE INDEX IF NOT EXISTS idx_users_online ON users(is_online);
CREATE INDEX IF NOT EXISTS idx_reactions_message ON reactions(message_id);

-- Insérer les salons par défaut
INSERT INTO rooms (name, description, created_by) VALUES 
    ('general', 'Chat général pour tous', 'system'),
    ('tech', 'Discussions techniques', 'system'),
    ('random', 'Sujets aléatoires', 'system'),
    ('support', 'Aide et support', 'system')
ON CONFLICT (name) DO NOTHING;

-- Donner les permissions à l'utilisateur de l'application
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chatuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO chatuser;
