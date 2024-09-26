

# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Conductores(Base):
    __tablename__ = 'conductores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    user = Column(String)
    password = Column(String)

    # Relación inversa desde TiposViaje
    tipos_viaje_conductor = relationship('TiposViaje', foreign_keys='TiposViaje.pk_id_conductor', back_populates='conductor')
    tipos_viaje_conductor_mini = relationship('TiposViaje', foreign_keys='TiposViaje.pk_id_conductor_mini', back_populates='conductor_mini')

class Grupos(Base):
    __tablename__ = 'grupos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)

class TiposViaje(Base):
    __tablename__ = 'tipos_viaje'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pk_grupo = Column(Integer, ForeignKey('grupos.id'))
    pk_id_conductor = Column(Integer, ForeignKey('conductores.id'))
    siguiente = Column(Integer)
    pk_id_conductor_mini = Column(Integer, ForeignKey('conductores.id'))

    __table_args__ = (
        UniqueConstraint('pk_grupo', 'pk_id_conductor', 'pk_id_conductor_mini', name='uq_grupo_siguiente'),
    )

    # Definir las relaciones con los conductores
    conductor = relationship('Conductores', foreign_keys=[pk_id_conductor], back_populates='tipos_viaje_conductor')
    conductor_mini = relationship('Conductores', foreign_keys=[pk_id_conductor_mini], back_populates='tipos_viaje_conductor_mini')

    # Definir relación con Master
    master = relationship('Master', back_populates='viaje')

class Master(Base):
    __tablename__ = 'master'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime)
    pk_viaje = Column(Integer, ForeignKey('tipos_viaje.id'))
    notas = Column(String)

    # Relación con TiposViaje
    viaje = relationship('TiposViaje', back_populates='master')
