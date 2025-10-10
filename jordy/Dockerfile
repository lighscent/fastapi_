# Stage 1: Container pour main.py
FROM python:3-slim AS main-app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 2: Container pour todo.py  
FROM python:3-slim AS todo-app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY todo.py ./

EXPOSE 8080

CMD ["uvicorn", "todo:app", "--host", "0.0.0.0", "--port", "8080"]
