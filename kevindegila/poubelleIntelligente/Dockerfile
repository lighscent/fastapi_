# FROM python:3-slim
FROM tensorflow/tensorflow:latest

WORKDIR /app

# Mettre à jour pip d'abord
RUN pip install --upgrade pip

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Affiche la version Python de manière visible dans le fichier log de Docker
RUN echo "===========================================" && \
    python --version && \
    echo "==========================================="

# Installer les dépendances une par une au lieu d'utiliser requirements.txt
# RUN pip install --no-cache-dir fastapi==0.115.0
RUN pip install --no-cache-dir fastapi
# RUN pip install --no-cache-dir "uvicorn[standard]==0.32.0"
RUN pip install --no-cache-dir "uvicorn[standard]"
# RUN pip install --no-cache-dir python-multipart==0.0.20
RUN pip install --no-cache-dir python-multipart
# RUN pip install --no-cache-dir streamlit==1.40.0 # ✅ Version compatible


COPY . .
COPY best_model.h5 /app/best_model.h5


EXPOSE 8000

CMD [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000" ]
