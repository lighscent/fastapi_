from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import FileResponse
import flet as ft
from typing import Union, List, Optional
from pydantic import BaseModel

import uvicorn


app = FastAPI(
    title="Ma super API ToDo",
    version="1.0.0",
    description="Ceci est une simple API pour une ToDo liste.",
)


class ToDo(BaseModel):
    id: int
    title: str
    desc: Optional[str] = None
    due_date: str
    completed: bool = False


class TodoResponse(BaseModel):
    source: str
    items: List[ToDo]
    total: int


store_todo = [
    ToDo(
        id=1,
        title="Acheter du lait",
        desc="Aller au supermarché et acheter du lait",
        due_date="2023-10-01",
    ),
    ToDo(
        id=2,
        title="Envoyer un email",
        desc="Envoyer un email à mon patron",
        due_date="2023-10-02",
    ),
]


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/", response_model=TodoResponse)
async def todos() -> dict:
    return {"source": "todo-app", "items": store_todo, "total": len(store_todo)}


@app.get("/{id}")
async def get_todo(
    id: int = Path(..., description="The ID of the todo to retrieve", gt=0)
) -> ToDo:
    try:
        return next(todo for todo in store_todo if todo.id == id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="ToDo not found")


@app.post("/todo", response_model=ToDo, status_code=201)
async def create_todo(todo: ToDo) -> ToDo:
    store_todo.append(todo)
    return todo


@app.put("/todo/{id}", response_model=ToDo)
async def update_todo(
    todo: ToDo,
    id: int = Path(..., description="The ID of the todo to update", gt=0),
) -> ToDo:
    try:
        search = next(t for t in store_todo if t.id == id)
        search.title = todo.title
        search.desc = todo.desc
        search.due_date = todo.due_date
        search.completed = todo.completed
        return search
    except StopIteration:
        raise HTTPException(status_code=404, detail="ToDo not found")

@app.delete("/todo/{id}")
async def delete_todo(id: int = Path(..., description="The ID of the todo to delete", gt=0))->dict:
    try:
        obj = store_todo.pop(id - 1)
        return {"deleted todo": obj}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"ToDo #{id} not found")

if __name__ == "__main__":
    uvicorn.run("todo:app", host="127.0.0.1", port=8080, reload=True)
    print("Ready.")
