"""
Router para gestión de ejercicios
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from database import get_db
from models import (
    Exercise, ExerciseResponse, ExerciseCreate, ExerciseUpdate, 
    User, GrupoMuscularEnum, NivelDificultadEnum, user_favorite_exercises
)
from routers.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises(
    grupo_muscular: Optional[GrupoMuscularEnum] = None,
    nivel_dificultad: Optional[NivelDificultadEnum] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener lista de ejercicios con filtros opcionales"""
    query = db.query(Exercise).filter(Exercise.is_active == True)
    
    # Filtros
    if grupo_muscular:
        query = query.filter(Exercise.grupo_muscular == grupo_muscular.value)
    
    if nivel_dificultad:
        query = query.filter(Exercise.nivel_dificultad == nivel_dificultad.value)
    
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                Exercise.nombre.ilike(search_term),
                Exercise.descripcion.ilike(search_term),
                Exercise.equipo_necesario.ilike(search_term)
            )
        )
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises

@router.get("/grupos-musculares")
async def get_muscle_groups():
    """Obtener lista de grupos musculares disponibles"""
    return {
        "grupos_musculares": [grupo.value for grupo in GrupoMuscularEnum]
    }

@router.get("/favoritos", response_model=List[ExerciseResponse])
async def get_favorite_exercises(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener ejercicios favoritos del usuario"""
    return current_user.ejercicios_favoritos

@router.post("/favoritos/{exercise_id}")
async def add_favorite_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Agregar ejercicio a favoritos"""
    # Verificar que el ejercicio existe
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Verificar si ya está en favoritos
    if exercise in current_user.ejercicios_favoritos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise already in favorites"
        )
    
    # Agregar a favoritos
    current_user.ejercicios_favoritos.append(exercise)
    db.commit()
    
    return {"message": "Exercise added to favorites"}

@router.delete("/favoritos/{exercise_id}")
async def remove_favorite_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remover ejercicio de favoritos"""
    # Verificar que el ejercicio existe
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Verificar si está en favoritos
    if exercise not in current_user.ejercicios_favoritos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise not in favorites"
        )
    
    # Remover de favoritos
    current_user.ejercicios_favoritos.remove(exercise)
    db.commit()
    
    return {"message": "Exercise removed from favorites"}

@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Obtener un ejercicio específico por ID"""
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.is_active == True
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    return exercise

@router.get("/grupo/{grupo_muscular}", response_model=List[ExerciseResponse])
async def get_exercises_by_muscle_group(
    grupo_muscular: GrupoMuscularEnum,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener ejercicios por grupo muscular específico"""
    exercises = db.query(Exercise).filter(
        Exercise.grupo_muscular == grupo_muscular.value,
        Exercise.is_active == True
    ).offset(skip).limit(limit).all()
    
    return exercises

# Endpoints administrativos (requieren permisos especiales en producción)
@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo ejercicio (admin)"""
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar ejercicio (admin)"""
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    update_data = exercise_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exercise, field, value)
    
    db.commit()
    db.refresh(db_exercise)
    return db_exercise