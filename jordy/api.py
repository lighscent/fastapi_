from fastapi import FastAPI, Path, HTTPException, Form
import flet as ft
from typing import Union, List, Optional
from pydantic import BaseModel

import uvicorn

app = FastAPI()

# get, put, post, delete


class CoordIn(BaseModel):
    pw: str
    lat: float
    lon: float
    zoom: Optional[int] = None
    desc: Optional[str] = None


class CoordOut(BaseModel):
    lat: float
    lon: float
    zoom: Optional[int] = None
    desc: Optional[str] = None


@app.get("/hi")
async def hello() -> dict:
    """Say hello

    Returns:
        dict: A greeting message
    """
    return {"msg": "Hi !"}


@app.get("/")
async def hello() -> dict:
    return {"msg": "Salut from api-app 123 !"}


@app.get("/component/{component_id}")
async def get_component(component_id: int) -> dict:
    return {"component_id": component_id}


# http://127.0.0.1:8000/component/?number=456&text=abc%20def
@app.get("/component/")
async def read_component(number: int, text: Optional[str]) -> dict:
    return {"number": number, "text": text}


@app.post("/position", response_model=CoordOut, response_model_exclude={"desc"})
async def create_position(coord: CoordIn) -> dict:
    return coord


@app.post("/position/form", response_model=CoordOut, response_model_exclude={"desc"})
async def create_position_form(
    pw: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    zoom: Optional[int] = Form(None),
    desc: Optional[str] = Form(None),
) -> dict:
    if pw != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"lat": lat, "lon": lon, "zoom": zoom, "desc": desc}


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
    print("Ready.")
