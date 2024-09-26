# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'

# Creación del motor de base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,         # Número de conexiones persistentes en el pool
    max_overflow=20,      # Número máximo de conexiones adicionales si el pool está lleno
    pool_timeout=30,      # Tiempo máximo en segundos que una conexión puede esperar antes de lanzar un timeout
    pool_recycle=1800,    # Reciclar conexiones después de 1800 segundos (30 minutos)
    pool_pre_ping=True    # Habilitar `pool_pre_ping` para detectar conexiones caídas
)

# Crea la clase base para los modelos
Base = declarative_base()

# Crea una sesión configurada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
