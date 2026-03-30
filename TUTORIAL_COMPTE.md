# 🚀 Tutoriel : Créer GitHub et Docker Hub

## 📋 **Étape 1 : Créer GitHub (Gratuit)**

### 1.1 Inscrivez-vous sur GitHub
1. Allez sur **https://github.com**
2. Cliquez sur **"Sign up"** (en haut à droite)
3. Remplissez le formulaire :
   - **Username** : Choisissez un nom (ex: `cira2025`, `dioufchat`, etc.)
   - **Email** : Votre email
   - **Password** : Choisissez un mot de passe fort
4. Cliquez **"Continue"**
5. Vérifiez votre email (vérifiez vos spams)

### 1.2 Créez votre Repository
1. Connectez-vous à GitHub
2. Cliquez sur **"+"** → **"New repository"**
3. Remplissez :
   - **Repository name** : `chat-simple`
   - **Description** : `Application de messagerie instantanée avec Flask et Docker`
   - ✅ **Public** (très important !)
4. Cliquez **"Create repository"**

---

## 🐳 **Étape 2 : Créer Docker Hub (Gratuit)**

### 2.1 Inscrivez-vous sur Docker Hub
1. Allez sur **https://hub.docker.com**
2. Cliquez sur **"Sign up"**
3. Choisissez **"Docker Hub"** (pas Docker Desktop)
4. Remplissez :
   - **Docker ID** : Le même que votre username GitHub
   - **Email** : Votre email
   - **Password** : Mot de passe
5. Vérifiez votre email

### 2.2 Créez votre Repository
1. Connectez-vous à Docker Hub
2. Cliquez sur **"Create repository"**
3. Remplissez :
   - **Namespace** : Votre username
   - **Repository name** : `chat-simple`
   - **Description** : `Chat application with Flask and Docker`
   - **Visibility** : Public
4. Cliquez **"Create"**

---

## 🔄 **Étape 3 : Pousser votre code sur GitHub**

### 3.1 Initialisez Git
Ouvrez un terminal dans votre dossier `DEVNET` :

```bash
git init
git add .
git commit -m "Initial commit - Chat Application"
```

### 3.2 Connectez à GitHub
```bash
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/chat-simple.git
git push -u origin main
```

**Remplacez `VOTRE_USERNAME` par votre vrai username GitHub !**

---

## 🐳 **Étape 4 : Construire et Push sur Docker Hub**

### 4.1 Construisez l'image
```bash
docker build -t VOTRE_USERNAME/chat-simple:latest .
```

### 4.2 Connectez-vous à Docker Hub
```bash
docker login
# Entrez votre username et mot de passe Docker Hub
```

### 4.3 Push l'image
```bash
docker push VOTRE_USERNAME/chat-simple:latest
```

---

## 📝 **Vos Liens Finaux**

Une fois terminé, vos liens seront :

**GitHub :**
```
https://github.com/VOTRE_USERNAME/chat-simple
```

**Docker Hub :**
```
https://hub.docker.com/r/VOTRE_USERNAME/chat-simple
```

---

## 🎯 **Pour le Tableau du Prof**

Copiez-collez ça avec VOS informations :

```
NOM : [Votre Nom]
PRENOM : [Votre Prénom]
DESCRIPTION : Application de messagerie instantanée développée avec Flask, PostgreSQL et Docker. Les utilisateurs peuvent se connecter avec un nom d'utilisateur, échanger des messages en temps réel, voir la liste des utilisateurs connectés et bénéficier d'une interface moderne avec animations.
LIEN GITHUB : https://github.com/VOTRE_USERNAME/chat-simple
LIEN DOCKER HUB : https://hub.docker.com/r/VOTRE_USERNAME/chat-simple
```

---

## 🆘 **Si vous êtes bloqué**

Dites-moi :
1. À quelle étape vous êtes bloqué ?
2. Quel username avez-vous choisi ?
3. Quel est votre email ?

Je vous aiderai en direct ! 💪

---

## ⏰ **Temps estimé**
- GitHub : 5 minutes
- Docker Hub : 5 minutes  
- Push code : 2 minutes
- Build Docker : 3 minutes
- **Total : 15 minutes maximum !**

**C'est super facile, vous allez voir !** 🚀
