"""
Modelos de base de datos para la API de Rutinas de Gym
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

Base = declarative_base()

# Tabla de relación muchos a muchos para ejercicios favoritos
user_favorite_exercises = Table(
    'user_favorite_exercises',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True)
)

class GrupoMuscularEnum(str, Enum):
    ABS = "abs"
    BICEPS = "biceps"
    ESPALDA = "espalda"
    GEMELOS = "gemelos"
    HOMBROS = "hombros"
    PECTORALES = "pectorales"
    PIERNAS = "piernas"
    TRICEPS = "triceps"

class NivelDificultadEnum(str, Enum):
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"

class CategoriaRutinaEnum(str, Enum):
    FUERZA = "fuerza"
    HIPERTROFIA = "hipertrofia"
    RESISTENCIA = "resistencia"
    DEFINICION = "definicion"
    FUNCIONAL = "funcional"

# Modelos SQLAlchemy (Base de datos)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    rutinas = relationship("Rutina", back_populates="owner")
    ejercicios_favoritos = relationship("Exercise", secondary=user_favorite_exercises, back_populates="usuarios_favoritos")

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    grupo_muscular = Column(String, nullable=False, index=True)  # GrupoMuscularEnum
    descripcion = Column(Text)
    instrucciones = Column(Text)
    nivel_dificultad = Column(String, default="intermedio")  # NivelDificultadEnum
    equipo_necesario = Column(String)
    imagen_url = Column(String)  # Ruta a la imagen
    musculos_secundarios = Column(String)  # Separados por comas
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    series = relationship("SerieEjercicio", back_populates="ejercicio")
    usuarios_favoritos = relationship("User", secondary=user_favorite_exercises, back_populates="ejercicios_favoritos")

class Rutina(Base):
    __tablename__ = "rutinas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    descripcion = Column(Text)
    categoria = Column(String, nullable=False)  # CategoriaRutinaEnum
    duracion_estimada = Column(Integer)  # en minutos
    nivel_dificultad = Column(String, default="intermedio")  # NivelDificultadEnum
    is_public = Column(Boolean, default=False)  # Si otros usuarios pueden verla
    is_template = Column(Boolean, default=False)  # Si es una plantilla predefinida
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    owner = relationship("User", back_populates="rutinas")
    series = relationship("SerieEjercicio", back_populates="rutina", cascade="all, delete-orphan")

class SerieEjercicio(Base):
    __tablename__ = "series_ejercicios"
    
    id = Column(Integer, primary_key=True, index=True)
    rutina_id = Column(Integer, ForeignKey("rutinas.id"), nullable=False)
    ejercicio_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    orden = Column(Integer, nullable=False)  # Orden del ejercicio en la rutina
    series = Column(Integer, nullable=False)
    repeticiones_min = Column(Integer)
    repeticiones_max = Column(Integer)
    peso = Column(Float)  # Opcional
    tiempo_descanso = Column(Integer)  # en segundos
    notas = Column(Text)  # Notas específicas para este ejercicio en la rutina
    
    # Relaciones
    rutina = relationship("Rutina", back_populates="series")
    ejercicio = relationship("Exercise", back_populates="series")

# Modelos Pydantic (Validación y Serialización)

# User schemas
class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Exercise schemas
class ExerciseBase(BaseModel):
    nombre: str
    grupo_muscular: GrupoMuscularEnum
    descripcion: Optional[str] = None
    instrucciones: Optional[str] = None
    nivel_dificultad: NivelDificultadEnum = NivelDificultadEnum.INTERMEDIO
    equipo_necesario: Optional[str] = None
    musculos_secundarios: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    instrucciones: Optional[str] = None
    nivel_dificultad: Optional[NivelDificultadEnum] = None
    equipo_necesario: Optional[str] = None
    musculos_secundarios: Optional[str] = None

class ExerciseResponse(ExerciseBase):
    id: int
    imagen_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# SerieEjercicio schemas
class SerieEjercicioBase(BaseModel):
    ejercicio_id: int
    orden: int
    series: int
    repeticiones_min: Optional[int] = None
    repeticiones_max: Optional[int] = None
    peso: Optional[float] = None
    tiempo_descanso: Optional[int] = None
    notas: Optional[str] = None

class SerieEjercicioCreate(SerieEjercicioBase):
    pass

class SerieEjercicioUpdate(BaseModel):
    orden: Optional[int] = None
    series: Optional[int] = None
    repeticiones_min: Optional[int] = None
    repeticiones_max: Optional[int] = None
    peso: Optional[float] = None
    tiempo_descanso: Optional[int] = None
    notas: Optional[str] = None

class SerieEjercicioResponse(SerieEjercicioBase):
    id: int
    rutina_id: int
    ejercicio: ExerciseResponse
    
    class Config:
        from_attributes = True

# Rutina schemas
class RutinaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: CategoriaRutinaEnum
    duracion_estimada: Optional[int] = None
    nivel_dificultad: NivelDificultadEnum = NivelDificultadEnum.INTERMEDIO
    is_public: bool = False

class RutinaCreate(RutinaBase):
    series: List[SerieEjercicioCreate] = []

class RutinaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[CategoriaRutinaEnum] = None
    duracion_estimada: Optional[int] = None
    nivel_dificultad: Optional[NivelDificultadEnum] = None
    is_public: Optional[bool] = None

class RutinaResponse(RutinaBase):
    id: int
    owner_id: int
    is_template: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    series: List[SerieEjercicioResponse] = []
    owner: UserResponse
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str