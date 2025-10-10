# fastpai

## https://www.youtube.com/watch?v=7D_0JTeaKWg&t=10s (2H)

## api-app & todo-app

* Dans un même Dockerfile
* venv si lancement manuel, utiliser requirements_api_toto.txt

## Mises en route

uvicorn api:app --reload

docker build -t fastapi_img:v0 .

docker run -p 8000:8000 fastapi_img:v0

OU

docker-compose up -d

Pour reconstruire
docker-compose up --build -d

### tortoise

