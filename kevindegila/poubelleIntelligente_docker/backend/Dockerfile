FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Affiche la version Python
RUN echo "===========================================" && \
    python --version && \
    echo "==========================================="

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
    
# NOTE: COPY . . est commenté pour le développement
# Les fichiers sont montés via volume dans docker-compose.dev.yml
# Pour la prod, utiliser docker-compose.prod.yml qui inclut le COPY

EXPOSE 8000

# Mode développement avec reload automatique
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
