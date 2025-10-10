from fastapi import FastAPI, Form, HTTPException
import uvicorn
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from unittest.util import _MAX_LENGTH

app = FastAPI(
    title="Tortoise API",
    description="An API to manage tortoises ORM",
    version="1.0.0",
)


class Todo(models.Model):
    id = fields.IntField(pk=True)
    todo = fields.CharField(max_length=250)
    due_date = fields.CharField(max_length=250)

    class PydanticMeta:
        pass


@app.post("/login/")
async def login(
    username: str = Form(..., description="(ie: **user**)"),
    password: str = Form(..., description="(ie: **pass**)"),
):
    if username == "user" and password == "pass":
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)

if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run("turtoise:app", host="127.0.0.1", port=8000, reload=True)
    print("Ready.")
