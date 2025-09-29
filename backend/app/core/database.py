from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

# Configuración de base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://spotify_user:spotify_pass@postgres:5432/spotify_analytics"
)

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Crear sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

def get_db():
    """
    Dependency para obtener sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Crear todas las tablas en la base de datos
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos creadas correctamente")
    except Exception as e:
        logger.error(f"Error creando tablas: {e}")
        raise