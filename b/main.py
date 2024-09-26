# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from typing import List, Optional

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/ping", response_model=str)
async def ping():
    return "pong"

# Rutas CRUD para Conductores
@app.post("/conductores/", response_model=schemas.Conductores)
def create_conductor(conductor: schemas.ConductoresCreate, db: Session = Depends(get_db)):
    db_conductor = models.Conductores(**conductor.dict())
    db.add(db_conductor)
    db.commit()
    db.refresh(db_conductor)
    return db_conductor

@app.get("/conductores/", response_model=List[schemas.Conductores])
def read_conductores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    conductores = db.query(models.Conductores).offset(skip).limit(limit).all()
    return conductores

# Puedes seguir creando rutas CRUD similares para `Grupos`, `TiposViaje` y `Master`
