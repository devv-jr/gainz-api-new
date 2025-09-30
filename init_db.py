"""
Script de inicialización para producción
"""
import os
from database import engine
from models import Base
from populate_all_exercises import populate_all_exercises, create_admin_user

def init_production_db():
    """Inicializar base de datos en producción"""
    print("🚀 Inicializando base de datos de producción...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas")
    
    # Solo poblar si no hay ejercicios
    from database import SessionLocal
    from models import Exercise
    
    db = SessionLocal()
    try:
        exercise_count = db.query(Exercise).count()
        if exercise_count == 0:
            print("📋 Poblando base de datos...")
            populate_all_exercises()
            create_admin_user()
        else:
            print(f"✅ Base de datos ya tiene {exercise_count} ejercicios")
    finally:
        db.close()
    
    print("🎉 Inicialización completa")

if __name__ == "__main__":
    init_production_db()