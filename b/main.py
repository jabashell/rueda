# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic import BaseModel
import models, schemas
from database import SessionLocal, engine
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import pytz

import uvicorn

# Configuración del contexto de la contraseña (usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Clave secreta y algoritmo para JWT
SECRET_KEY = "secret_key_example_123456"  # Debe ser única y secreta en producción 
#TODO
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Lista de orígenes permitidos (puedes añadir dominios específicos)
origins = [
    "http://localhost",
    "http://localhost:3000",  # Ejemplo: Si tienes un frontend en React corriendo en el puerto 3000
    "http://localhost:5173",  # Ejemplo: Si tienes un frontend en React corriendo en el puerto 3000
    "http://localhost:8000",
    "https://rueda-ide.vercel.app"   # Si deseas permitir un dominio en producción
]

# Añadir el middleware de CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes específicos
    allow_credentials=True,  # Permitir el uso de credenciales (cookies, cabeceras, etc.)
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeceras permitidas
)

# Dependencia de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuración del contexto de la contraseña (usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos Pydantic para definir esquemas
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener el usuario desde la "base de datos"
def get_user(username: str,  db: Session = Depends(get_db)):
    user = db.query(models.Conductores).filter(models.Conductores.user == username).first()
    if user:
        return user


@app.get("/ping", response_model=str)
async def ping():
    return "pong"

# Autenticar al usuario
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



# Función para crear el token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Ruta para generar el token
@app.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Ruta para comprobar si el token es válido

@app.get("/api/token_status", response_model=schemas.TokenStatus)
async def check_token_status(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"status": True}

@app.get("/api/grupos/", response_model=List[schemas.Grupo])
def get_grupos(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    groups = db.query(models.Grupos).all()

    return groups

@app.post("/api/viajes", response_model=List[schemas.ListaConductor])
def read_conductores(data: schemas.GetViajes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    ultimos_viajes = (
        db.query(models.Master)
        .join(models.TiposViaje)
        .filter(models.TiposViaje.pk_grupo == data.id_grupo)
        .order_by(models.Master.id.desc())
        .limit(data.num_entradas)
        .options(joinedload(models.Master.viaje).joinedload(models.TiposViaje.conductor))  # Cargar conductores
        .all()
    )
    l_ultimos_viajes = []
    for viaje in ultimos_viajes[::-1]:
        data_viaje = {  'fecha' : viaje.fecha, 
                        'nombre_conductor': viaje.viaje.conductor.nombre, 
                        'nombre_conductor_mini': viaje.viaje.conductor_mini.nombre,
                        'notas_viaje': viaje.notas,}
        l_ultimos_viajes.append(data_viaje)

    return l_ultimos_viajes

@app.post("/api/siguiente_conductor", response_model=schemas.SiguienteViaje)
def siguiente_conductor(data: schemas.GrupoViaje, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Devuelve el siguiente conductor para un grupo dado. """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    ultimo_viaje_grupo = (
        db.query(models.Master)
        .join(models.TiposViaje)
        .filter(models.TiposViaje.pk_grupo == data.id_grupo)
        .order_by(models.Master.id.desc())
        .options(joinedload(models.Master.viaje).joinedload(models.TiposViaje.conductor))  # Cargar conductores
        .first()
    )
    siguiente_viaje = db.query(models.TiposViaje).filter(models.TiposViaje.id == ultimo_viaje_grupo.pk_viaje).first()
    siguiente_conductor_tp = db.query(models.TiposViaje).filter(models.TiposViaje.id == siguiente_viaje.siguiente).first()
    siguiente_conductor = db.query(models.Conductores).filter(models.Conductores.id == siguiente_conductor_tp.pk_id_conductor).first()
    
    return {"id_siguiente_conductor"  : siguiente_viaje.siguiente, "nombre_siguiente_conductor": siguiente_conductor.nombre}



@app.post("/api/comprobar_fecha", response_model=schemas.DataExiste)
def comprobar_fecha(data: schemas.MasterBase, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Devuelve el siguiente conductor para un grupo dado. """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

        # Obtener la fecha que viene en UTC
    fecha_utc = data.fecha

    # Obtener la fecha que viene en la zona horaria local    # Convertir a la zona horaria local (CET/CEST)
    zona_horaria = pytz.timezone("Europe/Madrid")
    data.fecha = fecha_utc.astimezone(zona_horaria)
    
    data_existe = db.query(models.Master).filter(models.Master.fecha == data.fecha.strftime("%Y-%m-%d")).first()
    if data_existe:
        existe = {'existe': True}
        existe ['data'] = {}
        existe ["data"] ["fecha"] = data_existe.fecha
        existe ["data"] ["grupo"] = data_existe.viaje.grupo.descripcion
        existe ["data"] ["conductor"] = data_existe.viaje.conductor.nombre
    else:
        existe = {'existe': False}
    
    return existe






@app.post("/api/asignar_conductor", response_model=schemas.MasterBase)
def asignar_conductor(data: schemas.MasterBase, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Devuelve el siguiente conductor para un grupo dado. """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Obtener la fecha que viene en la zona horaria local    # Convertir a la zona horaria local (CET/CEST)
    # Como no consigo que la hora este correcto y pierdo 1 día al hacer el commit, le sumo 2 horas
    data.fecha += timedelta(hours=2)

    new_master = models.Master(**data.dict())
    db.add(new_master)
    db.commit()
    
    return {"fecha" : data.fecha, "pk_viaje": data.pk_viaje}


@app.post("/api/borrar_dia")
async def borrar_dia (data: schemas.Fecha, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Buscar el registro con la fecha específica
    data.fecha += timedelta(hours=2)
    record = db.query(models.Master).filter(models.Master.fecha == data.fecha.date()).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")

    # Eliminar el registro
    db.delete(record)
    db.commit()
    return {"detail" : "Fecha eliminada con éxito"}


@app.post("/api/actualizar_notas")
async def actualizar_notas (data: schemas.FechaNota, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Buscar el registro con la fecha específica
    data.fecha += timedelta(hours=2)
    # Buscar el registro en la tabla 'Master' con la fecha específica
   
    record = db.query(models.Master).filter(models.Master.fecha == data.fecha.date()).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")

    # Actualizar la notas del registro
    record.notas = data.notas_viaje
    db.commit()
    return {"detail" : "Nota actualizada con éxito"}


# Ruta para obtener información del usuario autenticado
@app.get("/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

# Rutas CRUD para Conductores
@app.post("/conductores/", response_model=schemas.Conductores)
def create_conductor(conductor: schemas.ConductoresCreate, db: Session = Depends(get_db)):
    db_conductor = models.Conductores(**conductor.dict())
    db.add(db_conductor)
    db.commit()
    db.refresh(db_conductor)

    return db_conductor

@app.get("/conductores/", response_model=List[schemas.ListaConductor])
def read_conductores(token: str = Depends(oauth2_scheme), skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    conductores = db.query(models.Conductores).offset(skip).limit(limit).all()
    ultimos_viajes = (
        db.query(models.Master)
        .join(models.TiposViaje)
        .filter(models.TiposViaje.pk_grupo == "1")
        .order_by(models.Master.id.desc())
        .limit(3)
        .options(joinedload(models.Master.viaje).joinedload(models.TiposViaje.conductor))  # Cargar conductores
        .all()
    )
    l_ultimos_viajes = []
    for viaje in ultimos_viajes:
        data_viaje = {'fecha' : viaje.fecha, 'nombre_conductor': viaje.viaje.conductor.nombre, 'nombre_conductor_mini': viaje.viaje.conductor_mini.nombre}
        l_ultimos_viajes.append(data_viaje)

    return l_ultimos_viajes



@app.get("/users", response_model=schemas.Conductores)
def get_users( db: Session = Depends(get_db)):
    user = db.query(models.Conductores).filter(models.Conductores.user == 'd').first()
    return user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)