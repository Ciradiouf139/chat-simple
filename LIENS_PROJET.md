# 🚀 Liens du Projet - Chat Simple Distribué

## 📦 **Liens d'Accès**

### **🔗 GitHub Repository**
```
https://github.com/[VOTRE_USERNAME]/chat-simple
```

### **🐳 Docker Hub Repository**
```
https://hub.docker.com/r/[VOTRE_USERNAME]/chat-simple
```

---

## 🌐 **Accès à l'Application**

### **🚀 Démo en Ligne (si disponible)**
```
http://demo.votredomaine.com
```

### **💻 Accès Local (après docker-compose up)**
- **Instance 1** : http://localhost:5000
- **Instance 2** : http://localhost:5001
- **API Statut** : http://localhost:5000/api/status

---

## 📋 **Instructions pour le Professeur**

### **1. Cloner le Projet**
```bash
git clone https://github.com/[VOTRE_USERNAME]/chat-simple.git
cd chat-simple
```

### **2. Lancer avec Docker**
```bash
docker-compose up --build
```

### **3. Accéder aux Applications**
- Ouvrez http://localhost:5000 dans votre navigateur
- Entrez un nom d'utilisateur (ex: "Professeur")
- Testez l'envoi de messages

### **4. Tester le Réseau Distribué**
- Ouvrez http://localhost:5001 dans un autre onglet
- Connectez-vous avec un autre nom
- Vérifiez que les messages apparaissent des deux côtés

---

## 🔧 **Commandes Utiles**

### **Vérifier les Conteneurs**
```bash
docker-compose ps
```

### **Voir les Logs**
```bash
docker-compose logs app
docker-compose logs app2
```

### **Inspecter le Réseau**
```bash
docker network ls
docker network inspect chat-simple_chat-network
```

### **Tester la Connexion**
```bash
docker-compose exec app ping app2
```

---

## 📊 **Monitoring**

### **API de Statut**
```bash
curl http://localhost:5000/api/status
curl http://localhost:5001/api/status
```

### **Base de Données**
- **Hôte** : localhost:5432
- **Base** : chatdb
- **Utilisateur** : chatuser
- **Mot de passe** : chatpass123

---

## 🎯 **Points de Démonstration**

### **✅ Fonctionnalités à Montrer**
1. **Page de connexion moderne**
2. **Interface de chat en temps réel**
3. **Liste des utilisateurs connectés**
4. **Messages persistants**
5. **Design responsive**

### **🌐 Aspect Réseau**
1. **Communication entre conteneurs**
2. **Résolution DNS automatique**
3. **Base de données partagée**
4. **Isolation des services**

### **🐳 Docker**
1. **Multi-conteneurs**
2. **Réseau Docker bridge**
3. **Volumes de persistance**
4. **Variables d'environnement**

---

## 📞 **Support**

Pour toute question ou problème :
- **GitHub Issues** : https://github.com/[VOTRE_USERNAME]/chat-simple/issues
- **Email** : [votre-email@exemple.com]

---

**🎉 Le projet est prêt pour la démonstration !**
