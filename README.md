[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=2000&pause=400&color=6366F1&center=true&vCenter=true&multiline=true&repeat=false&width=600&height=100&lines=Hey+%F0%9F%91%8B+I'm+GrCOTE7;Just+A+French+Dev+%F0%9F%9A%80)](https://github.com/GrCOTE7)

[![Website](https://img.shields.io/badge/cote7.com-6366F1?style=for-the-badge&logo=safari)](https://cote7.com) [![Instagram](https://img.shields.io/badge/Instagram-GC7-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/grcote7) [![GitHub followers](https://img.shields.io/github/followers/grcote7?style=for-the-badge&logo=github&color=6366F1)](https://github.com/grcote7?tab=followers)

[![Python >= 3.6.2](https://img.shields.io/badge/python-%3E%3D3.6.2-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

```mermaid
graph TD
    root --> app
    app --> models
    app --> views
    app --> templates
```

# FastAPI

Ce projet vise à explorer le développement d'architectures backend modernes avec **FastAPI**, **Python** (et éventuellement **Mojo** pour les performances de calcul intensif). 

## 📚 Documentation et Ressources

- 📘 **[Introduction à FastAPI & Exemples](./docs/fastapi_intro.md)** : Qu'est-ce que FastAPI, comment l'utiliser et le comparer.
- 🚀 **[Mojo vs Python](./docs/mojo_vs_python.md)** : Pourquoi Mojo pourrait être le futur pour les calculs intensifs.
- ⚖️ **[Django vs FastAPI](./docs/django_vs_fastapi.md)** : Comparatif et choix de l'architecture pour une plateforme multi-utilisateurs et crypto.
- 🤖 **[Estimation LLM en Local](./docs/llm_estimation.md)** : Plan et durée estimés pour créer et déployer un LLM minimaliste.
- 🎓 **[Tutoriels et Commandes Utiles](./docs/tutos_resources.md)** : Liens vidéos YouTube pour se former à FastAPI et astuces de commandes.

---

## 🛠️ Installation et Déploiement

### 1️⃣ Forker le projet
Fork [https://github.com/GrCOTE7/fastapi/fork](https://github.com/GrCOTE7/fastapi/fork) → Dans GH, avec *TON_USER_COMPTE*

### 2️⃣ Cloner en local
En CLI, dans le dossier de votre choix :
```bash
git clone git@github.com:TON_USER-COMPTE/PROJECT.git
cd PROJECT
```

### 3️⃣ Mettre en place l'environnement virtuel (.venv)
> **Note** : Utiliser Python 3.6.2 minimum (et 3.12 max).
> Exemple pour Windows : [Télécharger Python 3.12.10 (zip)](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.zip) et décompresser dans `C:\python312\`

```bash
# 1. Créer le virtual env
C:\python312\python.exe -m venv .venv

# 2. Activer le venv (Exemple)
.\.venv\Scripts\activate

# 3. Mettre à jour pip et installer les dépendances
python -m pip install --upgrade pip
pip install fastapi uvicorn scikit-image numpy scipy
# OU : pip install -r requirements.txt
```

### 4️⃣ Configuration de l'environnement
Renommez `.env_exemple` en `.env` et renseignez-y, si besoin, vos clés d'API (comme `MISTRAL_API_KEY`).
*(Vous pouvez en générer une sur [Mistral Console](https://console.mistral.ai/codestral/cli?workspace_dialog=apiKeys)).*

### 5️⃣ Enjoy ! 😊
```bash
# Lancement de FastAPI
uvicorn main:app --reload

# Autre exécution
python TheSCRIPT.py
```
