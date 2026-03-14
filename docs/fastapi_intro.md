# Introduction à FastAPI

Aujourd’hui c'est quoi FastAPI ?
FastAPI est un framework web moderne et ultra performant conçu pour créer des API RESTful avec Python, à partir de la version 3.6.2. Voici ce qui le rend si spécial :

## ⚡️ Caractéristiques principales
**Rapidité** : Comparable à Node.js ou Go grâce à son architecture basée sur Starlette pour le serveur web et Pydantic pour la validation des données.

**Asynchrone** : Gère des milliers de requêtes simultanées avec async/await.

**Documentation automatique** : Génère des interfaces interactives comme Swagger UI et Redoc grâce à OpenAPI.

**Validation des données** : Utilise les annotations de type Python pour sécuriser et valider les entrées.

**Facilité d’utilisation** : Très intuitif, avec une courbe d’apprentissage modérée et une réduction du temps de développement jusqu’à 40 %.

## 🧠 À quoi ça sert ?
- Créer des endpoints API rapidement.
- Déployer des modèles de machine learning (TensorFlow, PyTorch).
- Construire des microservices, des applications temps réel (chat, notifications), ou même des apps IoT.
- Intégrer facilement des bases de données comme SQLAlchemy ou MongoDB.

## 🥊 Comparaison avec Flask et Django
| Critère | FastAPI | Flask | Django REST |
|---|---|---|---|
| Performances | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Asynchrone | Oui | Non | Non |
| Documentation intégrée | Oui | Non | Non |
| Courbe d’apprentissage | Modérée | Facile | Complexe |

## 🧪 Exemple de base : une API qui dit bonjour

```python
# fichier: main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bonjour depuis FastAPI !"}
```

### 🛠️ Étapes pour exécuter ce code
Installer FastAPI et Uvicorn (le serveur ASGI rapide) :

```bash
pip install fastapi uvicorn
```

Lancer le serveur :

```bash
uvicorn main:app --reload
```

Accéder à l’API :
Va sur `http://127.0.0.1:8000` → tu verras `{"message": "Bonjour depuis FastAPI !"}`.
Et pour la doc auto : `http://127.0.0.1:8000/docs` → Swagger UI ✨

## 🔍 Problème courant : ERR_SSL_PROTOCOL_ERROR
Ce message indique que ton navigateur essaie de se connecter en HTTPS (`https://127.0.0.1:8000`) alors que Uvicorn ne sert que en HTTP par défaut (`http://127.0.0.1:8000`).

✅ **Solution simple** :
Ne mets pas `https://` devant !
👉 Dans ton navigateur, tape exactement ceci : `http://127.0.0.1:8000`
Et pour la documentation Swagger : `http://127.0.0.1:8000/docs`

## 🏗️ Les géants (Kraken, Coinbase, Binance) utilisent-ils FastAPI ?
Non, pas directement. Ces plateformes utilisent des architectures beaucoup plus complexes et sur mesure, souvent basées sur des technologies éprouvées à très grande échelle.

| Plateforme | Backend principal | Notes |
|---|---|---|
| Binance | C++ / Java / Go / Python | Très orientée performance, avec des microservices en Go et Java pour le trading haute fréquence. |
| Coinbase | Ruby on Rails / Go / Node.js | Backend historique en Ruby, mais Go est utilisé pour les services critiques. |
| Kraken | C++ / JavaScript / Rust / Go | Kraken Pro utilise des technos très bas niveau pour la rapidité, avec du Rust et du C++. |

Ces plateformes ne se basent pas sur des frameworks comme FastAPI, mais peuvent l’utiliser pour des services internes, des outils d’administration, ou des API secondaires.
FastAPI est excellent pour des projets rapides, scalables et bien documentés, mais il est basé sur Python, qui n’est pas le langage le plus rapide pour les systèmes de trading en temps réel.
Cependant, dans l'écosystème crypto, on retrouve FastAPI dans des bots de trading open-source, des interfaces API pour des wallets, ou des projets DeFi.
