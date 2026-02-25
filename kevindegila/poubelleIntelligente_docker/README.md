# Process

## Créer Ctnrs Docker

    * Supprimer l'ancienne image
    docker rmi fastapi_img:v0
    
    * Rebuild avec la nouvelle version
    <!-- docker build -t fastapi_backend:v0 . -->
    
    docker compose up --build
    
    On doit voir les fichiers dans le Cntnr
    docker exec -it fastapi_backend_dev ls -l /app

    
    * Test
    
    api-app :
    docker run -p 8000:8000 fastapi_img:v0
    todo-app :
    docker run -p 8000:8080 fastapi_img:v0
    
    (port_local:port_docker)

// 2do une structure complète dev/prod

.env :
Windows PowerShell
Code
$env:API_URL="http://api:8000"
Linux / macOS
Code
export API_URL=http://api:8000
Docker
docker exec -it streamlit_frontend_dev env

Makefile
Marche sous Linux et WSL2
Sinon, Goibash, après installation:

Télécharge make pour Windows :
https://gnuwin32.sourceforge.net/packages/make.htm
(prends le fichier make-3.81.exe)

Installe-le dans un dossier simple, par exemple :
C:\Program Files (x86)\GnuWin32\bin

Ajoute ce dossier au PATH Windows :

Ouvre Paramètres système avancés

Variables d’environnement

Édite Path

Ajoute :
C:\Program Files (x86)\GnuWin32\bin

Ferme et rouvre Git Bash

Teste :

Code
make --version

une optimisation de ton Dockerfile TensorFlow

une config VS Code pour développer dans le conteneur

----


Si tu veux, je peux t’aider à aller encore plus loin :

ajouter un reverse proxy Nginx ou Traefik

activer HTTPS automatiquement (Let’s Encrypt)

optimiser la taille de tes images

préparer un déploiement sur un VPS, Render, Railway, Cloud Run
