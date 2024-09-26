# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


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
######## eliminar




# Esquema del conductor para incluir solo los campos requeridos
class Conductor(BaseModel):
    nombre_conductor: str

    class Config:
        from_attributes = True

class ListaConductor(BaseModel):
    fecha: datetime
    nombre_conductor: str
    nombre_conductor_mini: str

   # Configuración de Pydantic para convertir `datetime.date` a string `YYYY-MM-DD`
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d')
        }

        from_attributes = True

# Esquema del viaje para incluir conductor y datos adicionales relevantes
class Viaje(BaseModel):
    conductor: Optional[Conductor]
    pk_id_conductor_mini: Optional[int]

    class Config:
        from_attributes = True

# Esquema de la respuesta principal con los campos requeridos
class ConductorMiniResponse(BaseModel):
    fecha: datetime
    nombre_conductor: Optional[str] = None
    nombre_conductor_mini: Optional[str] = None

    class Config:
        from_attributes = True


class ConductoresBase(BaseModel):
    nombre: str
    user: str
    password: str
    hashed_password: str

class ConductoresCreate(ConductoresBase):
    pass

class Conductores(ConductoresBase):
    id: int
    class Config:
        from_attributes = True

class GruposBase(BaseModel):
    descripcion: str

class GruposCreate(GruposBase):
    pass


class Grupos(GruposBase):
    id: int
    class Config:
        from_attributes = True

class Grupo(GruposBase):
    id: int

class TiposViajeBase(BaseModel):
    pk_grupo: int
    pk_id_conductor: int
    siguiente: Optional[int] = None
    pk_id_conductor_mini: Optional[int] = None

class TiposViajeCreate(TiposViajeBase):
    pass

class TiposViaje(TiposViajeBase):
    id: int
    class Config:
        from_attributes = True

class MasterBase(BaseModel):
    fecha: datetime
    pk_viaje: int
    notas: Optional[str] = None

class MasterCreate(MasterBase):
    pass

class Master(MasterBase):
    id: int
    class Config:
        from_attributes = True
