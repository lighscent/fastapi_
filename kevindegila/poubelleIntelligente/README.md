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
    