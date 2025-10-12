from pyexpat import model
from annotated_types import T
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models import Todo, Todo_Pydantic, TodoIn_Pydantic
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
import sqlite3
import uvicorn


class Message(BaseModel):
    message: str


app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
)


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/hi")
async def hello():
    return {"message": "Hello World"}


@app.get("/infos")
async def root() -> dict:
    return {
        "source": "todo-app",
        "message": "Todo API is running",
        "endpoints": ["/docs", "/todo", "/todo/{todo_id}"],
    }


@app.get("/", response_model=dict)
async def get_all_todos():
    all_todos = await Todo_Pydantic.from_queryset(Todo.all())
    return {"source": "todo-app", "items": all_todos, "count": len(all_todos)}


@app.get("/todo/{todo_id}", response_model=Todo_Pydantic)
async def get_todo(todo_id: int):
    # ✅ Debug pour voir ce qui arrive
    print(f"Received todo_id: {todo_id}, type: {type(todo_id)}")
    try:
        return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")


@app.post("/todo", response_model=Todo_Pydantic)
async def create_todo(todo: TodoIn_Pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)


@app.put("/todo/{todo_id}", response_model=Todo_Pydantic)
async def update_todo(todo_id: int, todo: TodoIn_Pydantic):
    try:
        await Todo.filter(id=todo_id).update(**todo.dict(exclude_unset=True))
        return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")


@app.delete(
    "/todo/{todo_id}",
    response_model=Message,
    responses={404: {"model": Message}},
)
async def delete_todo(id: int):
    delete_obj = await Todo.filter(id=id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")
    return Message(message=f"Successfully deleted todo #{id}")


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    print("Ready.")
