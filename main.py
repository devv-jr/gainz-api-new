"""
Aplicación principal FastAPI para Gainz API
"""
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

# Importar módulos locales
from database import engine, get_db
from models import Base
from routers import auth, users, exercises, routines

# Cargar variables de entorno
load_dotenv()

# Crear tablas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="Gainz API",
    description="API para gestión de rutinas de gimnasio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos para las imágenes
app.mount("/images", StaticFiles(directory="images"), name="images")

# Incluir routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["Exercises"])
app.include_router(routines.router, prefix="/api/v1/routines", tags=["Routines"])

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Bienvenido a Gainz API 💪",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-09-29"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )