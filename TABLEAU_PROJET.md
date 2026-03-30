# 📋 Informations pour le Tableau du Professeur

## 🎯 **Copiez-Collez ces informations dans votre tableau**

### **NOM** : [Votre Nom]
### **PRENOM** : [Votre Prénom]

### **DESCRIPTION** :
Application de messagerie instantanée développée avec Flask, PostgreSQL et Docker. Les utilisateurs peuvent se connecter avec un nom d'utilisateur, échanger des messages en temps réel, voir la liste des utilisateurs connectés et bénéficier d'une interface moderne avec animations. L'application est déployée sur 2 instances Docker communicantes via un réseau bridge pour démontrer l'aspect distribué.

### **LIEN GITHUB** :
https://github.com/[VOTRE_USERNAME]/chat-simple

### **LIEN DOCKER HUB** :
https://hub.docker.com/r/[VOTRE_USERNAME]/chat-simple

---

## 🔧 **Étapes à suivre**

### **1. Remplacer [VOTRE_USERNAME]**
- Remplacez `[VOTRE_USERNAME]` par votre vrai nom d'utilisateur GitHub
- Exemple : si votre username est "alice2025", mettez "alice2025"

### **2. Remplacer [Votre Nom] et [Votre Prénom]**
- Mettez vos vrais noms

### **3. Créer le Repository GitHub**
1. Allez sur https://github.com
2. Cliquez sur "New repository"
3. Nom : `chat-simple`
4. Description : `Application de messagerie instantanée avec Flask et Docker`
5. Public ✅
6. Cliquez sur "Create repository"

### **4. Pousser votre code**
```bash
# Dans votre terminal
git init
git add .
git commit -m "Initial commit - Chat Application"
git branch -M main
git remote add origin https://github.com/[VOTRE_USERNAME]/chat-simple.git
git push -u origin main
```

### **5. Créer le Docker Hub**
1. Allez sur https://hub.docker.com
2. Cliquez "Create Repository"
3. Namespace : [VOTRE_USERNAME]
4. Repository name : `chat-simple`
5. Description : `Chat application with Flask and Docker`
6. Visibility : Public
7. Cliquez "Create"

### **6. Construire et Push l'image**
```bash
# Build l'image
docker build -t [VOTRE_USERNAME]/chat-simple:latest .

# Push sur Docker Hub
docker push [VOTRE_USERNAME]/chat-simple:latest
```

---

## 📝 **Exemple Complet à Copier**

*(Remplacez juste les informations entre crochets)*

---

**NOM** : [Votre Nom de famille]
**PRENOM** : [Votre Prénom]
**DESCRIPTION** : Application de messagerie instantanée développée avec Flask, PostgreSQL et Docker. Les utilisateurs peuvent se connecter avec un nom d'utilisateur, échanger des messages en temps réel, voir la liste des utilisateurs connectés et bénéficier d'une interface moderne avec animations. L'application est déployée sur 2 instances Docker communicantes via un réseau bridge pour démontrer l'aspect distribué.
**LIEN GITHUB** : https://github.com/[VOTRE_USERNAME]/chat-simple
**LIEN DOCKER HUB** : https://hub.docker.com/r/[VOTRE_USERNAME]/chat-simple

---

## 🚀 **Vérification Finale**

Une fois que vous avez rempli :
1. **Testez les liens** - ils doivent fonctionner
2. **Vérifiez GitHub** - le code doit être visible
3. **Vérifiez Docker Hub** - l'image doit apparaître
4. **Testez la démo** - `docker-compose up --build`

## 🎯 **Si vous avez besoin d'aide**

Dites-moi :
- Quel est votre username GitHub ?
- Quels sont vos nom et prénom ?
- Quelle étape vous bloque ?

Je vous aiderai pas à pas ! 💪
