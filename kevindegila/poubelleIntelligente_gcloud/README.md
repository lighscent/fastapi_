# Process

## Install venv

    python -m venv .venv
    
    cd dossier
    
    .\.venv\Scripts\activate
    
    pip install -r requirements.txt
    
    OU:
    pip install fastapi
    pip install "uvicorn[standard]"
    etc...

## Lancer CLIs

    uvicorn api:app --reload
    → http://127.0.0.1:8000
    → http://127.0.0.1:8000/docs
    
    streamlit run frontend.py
    streamlit run frontend.py --server.runOnSave=true --server.fileWatcherType=auto
    → http://localhost:8501

## Créer Dockerfile

    docker build -t fastapi_img:v0 .
    
    docker run -p 8000:8000 fastapi_img:v0
    
    (port_local:port_docker)

## gcloug

    Prérequis: gcloud CLI installé en local
    Dans GCP nouvelle app (Un nom tout en minuqcule - ex.: fastapi)
    (GPC va lui attribuer name, par ex. fastapi-473910)

    1. 🔧 Sélectionner le bon projet
    
    gcloud config set project fastapi-473910

    2. 🏗️ Créer le dépôt Artifact Registry

    ```
    gcloud artifacts repositories create fastapi-repo \
  --repository-format=docker \
  --location=europe-west1 \
  --description="Dépôt pour mes images FastAPI"
    ```

    3. 🔐 Configurer Docker pour l’authentification

    gcloud auth configure-docker europe-west1-docker.pkg.dev

    4. 🏷️ taguer ton image locale - Si image docker locale fastapi_img:v0 :

    docker tag fastapi_img:v0 europe-west1-docker.pkg.dev/fastapi-473910/fastapi-repo/fastapi_img:v0

    5. 📤 Pousser l’image vers Artifact Registry :
    
    docker push europe-west1-docker.pkg.dev/fastapi-473910/fastapi-repo/fastapi_img:v0

    ✅ Vérif :
    
    gcloud artifacts docker images list europe-west1-docker.pkg.dev/fastapi-473910/fastapi-repo

## Mapper un domaine
    
    1. 🔐 Valider la propriété du domaine
    Tu es déjà sur la bonne voie. Chez Bookmyname, ajoute un enregistrement DNS de type TXT :
    
    Nom : @ ou vide (selon l’interface)
    
    Type : TXT
    
    Valeur :
    
    Code
    google-site-verification=EMTs8mfzWAZU2OGqFNTJVcCaoEyZFeBNjqig9SO4SBM
    💡 Attends quelques minutes à quelques heures, puis clique sur Valider dans la Search Console ou dans la console GCP (section "Domaines vérifiés").
    
    2. 🌐 Créer le mapping de domaine vers Cloud Run
    Une fois le domaine validé, tu peux le lier à ton service Cloud Run :
    
    bash
    gcloud run domain-mappings create \
      --service=fastapi-img \
      --domain=c57.fr \
      --region=europe-west1
    Cela crée un lien entre c57.fr et ton service fastapi-img.
    
    3. 🧭 Ajouter l’enregistrement DNS CNAME ou A
    Après la commande ci-dessus, GCP te donnera une cible DNS (souvent un CNAME comme ghs.googlehosted.com ou un nom spécifique à Cloud Run).
    
    Chez Bookmyname, ajoute :
    
    Nom : @ (pour le domaine racine) ou www si tu veux www.c57.fr
    
    Type : CNAME
    
    Valeur : la cible donnée par GCP (ex. ghs.googlehosted.com)
    
    🧠 Bonus : rediriger www.c57.fr vers c57.fr
    Tu peux aussi ajouter un second mapping :
    
    bash
    gcloud run domain-mappings create \
      --service=fastapi-img \
      --domain=www.c57.fr \
      --region=europe-west1
    Et dans Bookmyname :
  
    www → CNAME vers la même cible
    
    📚 Référence officielle
    Tu peux suivre le guide complet ici : 👉 Mapping custom domains with Cloud Run
