# FROM python:3-slim
FROM python:3.12-slim

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

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
