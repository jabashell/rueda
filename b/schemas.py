# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ConductoresBase(BaseModel):
    nombre: str
    user: str
    password: str

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
