from ast import mod
from fastapi import FastAPI, Form, HTTPException
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
import uvicorn

# from unittest.util import _MAX_LENGTH

app = FastAPI(
    title="Tortoise API",
    description="An API to manage tortoises ORM",
    version="1.0.0",
)

class LoginRequest(BaseModel):
    username: str
    password: str


# api classic answer
@app.post("/log_in_api/", response_model=LoginRequest)
async def login(credentitials: LoginRequest) -> dict:
    if credentitials.username == "user" and credentitials.password == "pass":
        return {"username": credentitials.username, "password": credentitials.password}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# form answer
@app.post("/login/")
async def login(
    username: str = Form(..., description="(ie: **user**)"),
    password: str = Form(..., description="(ie: **pass**)"),
) -> dict:
    if username == "user" and password == "pass":
        return {"message": "Login user successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run("turtoise_form:app", host="127.0.0.1", port=8000, reload=True)
    print("Ready.")
