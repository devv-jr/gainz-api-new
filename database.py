"""
Configuración de la base de datos y conexiones
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URL de base de datos (Neon PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno")

# Configuración específica para Neon
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Importante para conexiones de larga duración
    pool_recycle=300,    # Reciclar conexiones cada 5 minutos
    echo=False           # Cambiar a True para debug SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar la conexión
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT version();")
            version = result.fetchone()[0]
            print(f"✅ Conexión exitosa a Neon PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"❌ Error conectando a Neon: {e}")
        return False

if __name__ == "__main__":
    test_connection()
