# Process

python -m venv .venv

cd dossier

.\.venv\Scripts\activate

pip install fastapi
pip install "uvicorn[standard]"
etc... OU:

pip install -r requirements.txt

Lancer CLIs:

uvicorn api:app --reload
→ http://127.0.0.1:8000

streamlit run frontend.py
→ http://127.0.0.1:8000/docs

Créer Dockerfile

docker build -t fastapi_img:v0 .

docker run -p 8000:8000 fastapi_img:v0

(port_local:port_docker)
