# 📚 Instructions pour le Professeur

## 🎯 **Présentation du Projet**

### **Étudiant**
- **Nom** : [Votre Nom Complet]
- **Classe** : L3 RI - ISI Keur Massar
- **Projet** : Chat Simple Distribué

---

## 🚀 **Accès Rapide**

### **🔗 Liens Principaux**
- **GitHub** : https://github.com/[VOTRE_USERNAME]/chat-simple
- **Docker Hub** : https://hub.docker.com/r/[VOTRE_USERNAME]/chat-simple

### **🌐 Lancement en 1 Commande**
```bash
git clone https://github.com/[VOTRE_USERNAME]/chat-simple.git
cd chat-simple
docker-compose up --build
```

### **📱 Accès Immédiat**
- **Chat 1** : http://localhost:5000
- **Chat 2** : http://localhost:5001

---

## 🎪 **Scénario de Démonstration**

### **Étape 1 : Lancement**
```bash
# Le prof lance ces commandes
docker-compose up --build
```

### **Étape 2 : Test du Chat**
1. **Ouvrir 2 onglets navigateur**
2. **Onglet 1** : http://localhost:5000 → "Alice"
3. **Onglet 2** : http://localhost:5001 → "Bob"
4. **Alice envoie** : "Bonjour Professeur !"
5. **Bob reçoit** le message en temps réel
6. **Bob répond** : "Bonjour Alice !"

### **Étape 3 : Vérification Réseau**
```bash
# Dans un nouveau terminal
docker-compose exec app ping app2
# Vérifie la communication entre conteneurs
```

---

## 📊 **Points Clés à Montrer**

### **🎨 Design Moderne**
- Page de connexion avec animations
- Interface de chat professionnelle
- Bulles de messages stylisées
- Avatars et indicateurs de statut

### **🌐 Aspect Réseau**
- **2 instances** qui communiquent
- **Base de données partagée**
- **Résolution DNS automatique**
- **Isolation des services**

### **🐳 Docker**
- **Multi-conteneurs** fonctionnels
- **Réseau bridge** configuré
- **Volumes** pour la persistance
- **Variables d'environnement**

---

## 🔍 **Vérification Technique**

### **API de Statut**
```bash
curl http://localhost:5000/api/status
# Réponse attendue : {"status": "online", "timestamp": "...", "instance": "instance1"}
```

### **Base de Données**
```bash
docker-compose exec db psql -U chatuser -d chatdb -c "SELECT COUNT(*) FROM messages;"
# Vérifie que les messages sont bien stockés
```

### **Réseau Docker**
```bash
docker network inspect chat-simple_chat-network
# Montre la configuration du réseau
```

---

## 🎉 **Conclusion**

Ce projet répond **parfaitement** à toutes les exigences de l'examen DEVNET :

1. ✅ **Application Flask** fonctionnelle
2. ✅ **Base de données** conteneurisée  
3. ✅ **Docker** multi-conteneurs
4. ✅ **Réseau** distribué
5. ✅ **Design** professionnel
6. ✅ **Documentation** complète

**Le projet est prêt pour l'évaluation !** 🚀
