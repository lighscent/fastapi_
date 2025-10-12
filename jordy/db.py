from atexit import register
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from datetime import datetime

DATABASE_URL = "sqlite:///./store.db"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

# ✅ Syntaxe SQLAlchemy correcte
users_table = sqlalchemy.Table(  # ✅ Renommé pour éviter le conflit
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),  # ✅ Syntaxe correcte
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()
    print("Connected to the database.")

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()
    print("Disconnected from the database.")

# ✅ Classe avec BaseModel
class Register(BaseModel):
    id: int
    name: str
    created_at: datetime
    
class RegisterIn(BaseModel):
    name: str = Field(..., example="John Doe")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
@app.post("/register/", response_model=Register)
async def create_user(user_data: RegisterIn):  # ✅ Pas de Depends() pour un body
    query = users_table.insert().values(
        name=user_data.name,
        created_at=datetime.utcnow()  # ✅ Appel de fonction
    )
    record_id = await database.execute(query)
    
    # Récupérer l'enregistrement créé
    query = users_table.select().where(users_table.c.id == record_id)
    row = await database.fetch_one(query)
    
    return Register(**row)  # ✅ Conversion en modèle Pydantic

# ✅ Endpoint pour lister tous les utilisateurs
@app.get("/register/", response_model=List[Register])
async def get_all_users():
    query = users_table.select()
    rows = await database.fetch_all(query)
    return [Register(**row) for row in rows]

# ✅ Endpoint pour récupérer un utilisateur par ID
@app.get("/register/{user_id}", response_model=Register)
async def get_one(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    row = await database.fetch_one(query)
    if row is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return Register(**row)

@app.get('/register/', response_model=List[Register])
async def get_all():
    query = register().select()
    all_get = await database.fetch_all(query)
    # return [Register(**row) for row in all_get] # //2ar #IA
    return all_get

@app.put("/register/{id}", response_model=Register)
async def update_user(id: int, user_data: RegisterIn):
    query = users_table.update().where(users_table.c.id == id).values(
        name=user_data.name,
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    
    # Récupérer l'enregistrement mis à jour
    query = users_table.select().where(users_table.c.id == id)
    row = await database.fetch_one(query)
    
    if row is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    
    return Register(**row)

@app.delete(  "/register/{id}", response_model=Register)
async def delete_user(id: int):
    query = users_table.delete().where(users_table.c.id == id)
    result = await database.execute(query)
    if result == 0:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
  