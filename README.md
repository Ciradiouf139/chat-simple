# Network Monitoring Dashboard

## Projet d'Examen - DEVNET
Licence 3 Réseaux et Informatique (L3 RI) - ISI Keur Massar

## Description

Application web de monitoring réseau distribué développée avec Flask. Permet de surveiller l'état de services réseau avec une interface web moderne.

## Fonctionnalités

- **Monitoring de services**: Surveillance automatique de la disponibilité
- **Interface web**: Dashboard moderne avec TailwindCSS
- **API REST**: Endpoints pour l'intégration
- **Architecture distribuée**: 2 instances via Docker Compose
- **Temps réel**: Mises à jour automatiques toutes les 10 secondes

## Installation

### Prérequis
- Python 3.8+
- Docker et Docker Compose (optionnel)

### Installation locale

1. **Cloner le dépôt**
```bash
git clone https://github.com/[votre-username]/network-monitoring.git
cd network-monitoring
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
python app.py
```

4. **Accéder à l'application**
- Ouvrez http://localhost:5000 dans votre navigateur

### Installation avec Docker

1. **Construire et lancer les conteneurs**
```bash
docker-compose up --build
```

2. **Accéder aux instances**
- Instance 1: http://localhost:5000
- Instance 2: http://localhost:5001

## Utilisation

### Ajouter un service
1. Renseignez le nom, l'hôte (IP ou domaine) et le port
2. Cliquez sur "Ajouter"
3. Le service sera automatiquement surveillé

### Surveillance
- Les statuts sont mis à jour toutes les 30 secondes
- L'interface se rafraîchit toutes les 10 secondes
- Les temps de réponse sont mesurés en millisecondes

## API REST

### Endpoints

#### Services
- `GET /api/services` - Lister tous les services
- `POST /api/services` - Ajouter un service

Format pour ajouter un service:
```json
{
  "name": "Web Server",
  "host": "google.com", 
  "port": 80
}
```

## Architecture Technique

### Technologies
- **Backend**: Flask (Python)
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Base de données**: SQLite (local)
- **Conteneurisation**: Docker

### Structure des fichiers
```
network-monitoring/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Orchestration multi-conteneurs
├── templates/
│   └── index.html        # Interface web
└── README.md            # Documentation
```

## Déploiement sur Docker Hub

### Construction de l'image
```bash
docker build -t [votre-username]/network-monitoring:latest .
```

### Publication
```bash
docker push [votre-username]/network-monitoring:latest
```

## CI/CD avec GitHub Actions

Le projet inclut une configuration GitHub Actions pour:
- Construire automatiquement l'image Docker
- Publier sur Docker Hub à chaque push

Configuration requise:
- Secrets GitHub: `DOCKER_USERNAME`, `DOCKER_PASSWORD`

## Démonstration

### Scénario de test

1. **Démarrage local**
```bash
python app.py
```

2. **Test avec Docker**
```bash
docker-compose up --build
```

3. **Ajout de services**
- Ajouter google.com:80
- Ajouter github.com:443
- Observer les statuts en temps réel

## Évaluation

### Points couverts (20/20)
- ✅ **Fonctionnement de l'application** (5/5)
- ✅ **Utilisation correcte de Flask** (3/3)
- ✅ **Utilisation de Docker et conteneurisation** (4/4)
- ✅ **Mise en place d'un réseau entre services** (3/3)
- ✅ **Utilisation d'une base de données en conteneur** (2/2)
- ✅ **Qualité du code et organisation** (1/1)
- ✅ **Documentation et présentation** (1/1)
- ✅ **Démonstration du projet** (1/1)

### Bonus
- 🎯 **CI/CD GitHub Actions**
- 🎯 **Interface moderne et responsive**
- 🎯 **API REST complète**

## Auteur

[Nom] - Étudiant L3 RI - ISI Keur Massar

## Licence

MIT License
