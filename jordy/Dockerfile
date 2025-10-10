# Stage 1: Container pour main.py
FROM python:3-slim AS api-app

WORKDIR /app

COPY requirements_api_todo.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api.py ./

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 2: Container pour todo.py  
FROM python:3-slim AS todo-app

WORKDIR /app

COPY requirements_api_todo.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY todo.py ./

EXPOSE 8080

CMD ["uvicorn", "todo:app", "--host", "0.0.0.0", "--port", "8080"]
