"""
Router para gestión de rutinas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from database import get_db
from models import (
    Rutina, RutinaResponse, RutinaCreate, RutinaUpdate,
    SerieEjercicio, SerieEjercicioCreate, SerieEjercicioUpdate, SerieEjercicioResponse,
    User, Exercise, CategoriaRutinaEnum, NivelDificultadEnum
)
from routers.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[RutinaResponse])
async def get_routines(
    categoria: Optional[CategoriaRutinaEnum] = None,
    nivel_dificultad: Optional[NivelDificultadEnum] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener rutinas del usuario actual y públicas con filtros"""
    query = db.query(Rutina).filter(
        or_(
            Rutina.owner_id == current_user.id,  # Rutinas del usuario
            Rutina.is_public == True  # Rutinas públicas
        )
    )
    
    # Filtros
    if categoria:
        query = query.filter(Rutina.categoria == categoria.value)
    
    if nivel_dificultad:
        query = query.filter(Rutina.nivel_dificultad == nivel_dificultad.value)
    
    if is_public is not None:
        query = query.filter(Rutina.is_public == is_public)
    
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                Rutina.nombre.ilike(search_term),
                Rutina.descripcion.ilike(search_term)
            )
        )
    
    rutinas = query.offset(skip).limit(limit).all()
    return rutinas

@router.get("/mis-rutinas", response_model=List[RutinaResponse])
async def get_my_routines(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener solo las rutinas del usuario actual"""
    rutinas = db.query(Rutina).filter(Rutina.owner_id == current_user.id).all()
    return rutinas

@router.get("/categorias")
async def get_routine_categories():
    """Obtener categorías de rutinas disponibles"""
    return {
        "categorias": [categoria.value for categoria in CategoriaRutinaEnum]
    }

@router.get("/plantillas", response_model=List[RutinaResponse])
async def get_routine_templates(
    categoria: Optional[CategoriaRutinaEnum] = None,
    nivel_dificultad: Optional[NivelDificultadEnum] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Obtener rutinas plantilla (predefinidas)"""
    query = db.query(Rutina).filter(Rutina.is_template == True)
    
    if categoria:
        query = query.filter(Rutina.categoria == categoria.value)
    
    if nivel_dificultad:
        query = query.filter(Rutina.nivel_dificultad == nivel_dificultad.value)
    
    plantillas = query.offset(skip).limit(limit).all()
    return plantillas

@router.post("/", response_model=RutinaResponse, status_code=status.HTTP_201_CREATED)
async def create_routine(
    rutina: RutinaCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nueva rutina"""
    # Crear la rutina
    rutina_data = rutina.dict(exclude={"series"})
    db_rutina = Rutina(**rutina_data, owner_id=current_user.id)
    
    db.add(db_rutina)
    db.commit()
    db.refresh(db_rutina)
    
    # Agregar series de ejercicios
    for serie_data in rutina.series:
        # Verificar que el ejercicio existe
        ejercicio = db.query(Exercise).filter(Exercise.id == serie_data.ejercicio_id).first()
        if not ejercicio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exercise with id {serie_data.ejercicio_id} not found"
            )
        
        db_serie = SerieEjercicio(**serie_data.dict(), rutina_id=db_rutina.id)
        db.add(db_serie)
    
    db.commit()
    db.refresh(db_rutina)
    return db_rutina

@router.get("/{rutina_id}", response_model=RutinaResponse)
async def get_routine(
    rutina_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener una rutina específica"""
    rutina = db.query(Rutina).filter(
        Rutina.id == rutina_id,
        or_(
            Rutina.owner_id == current_user.id,
            Rutina.is_public == True
        )
    ).first()
    
    if not rutina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    return rutina

@router.put("/{rutina_id}", response_model=RutinaResponse)
async def update_routine(
    rutina_id: int,
    rutina_update: RutinaUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar rutina (solo el propietario)"""
    db_rutina = db.query(Rutina).filter(
        Rutina.id == rutina_id,
        Rutina.owner_id == current_user.id
    ).first()
    
    if not db_rutina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    update_data = rutina_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_rutina, field, value)
    
    db.commit()
    db.refresh(db_rutina)
    return db_rutina

@router.delete("/{rutina_id}")
async def delete_routine(
    rutina_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Eliminar rutina (solo el propietario)"""
    db_rutina = db.query(Rutina).filter(
        Rutina.id == rutina_id,
        Rutina.owner_id == current_user.id
    ).first()
    
    if not db_rutina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    db.delete(db_rutina)
    db.commit()
    return {"message": "Routine deleted successfully"}

@router.post("/{rutina_id}/duplicar", response_model=RutinaResponse)
async def duplicate_routine(
    rutina_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Duplicar una rutina (crear copia personal)"""
    # Buscar rutina original
    rutina_original = db.query(Rutina).filter(
        Rutina.id == rutina_id,
        or_(
            Rutina.owner_id == current_user.id,
            Rutina.is_public == True
        )
    ).first()
    
    if not rutina_original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    # Crear nueva rutina
    nueva_rutina = Rutina(
        nombre=f"{rutina_original.nombre} (Copia)",
        descripcion=rutina_original.descripcion,
        categoria=rutina_original.categoria,
        duracion_estimada=rutina_original.duracion_estimada,
        nivel_dificultad=rutina_original.nivel_dificultad,
        is_public=False,
        is_template=False,
        owner_id=current_user.id
    )
    
    db.add(nueva_rutina)
    db.commit()
    db.refresh(nueva_rutina)
    
    # Copiar series de ejercicios
    for serie_original in rutina_original.series:
        nueva_serie = SerieEjercicio(
            rutina_id=nueva_rutina.id,
            ejercicio_id=serie_original.ejercicio_id,
            orden=serie_original.orden,
            series=serie_original.series,
            repeticiones_min=serie_original.repeticiones_min,
            repeticiones_max=serie_original.repeticiones_max,
            peso=serie_original.peso,
            tiempo_descanso=serie_original.tiempo_descanso,
            notas=serie_original.notas
        )
        db.add(nueva_serie)
    
    db.commit()
    db.refresh(nueva_rutina)
    return nueva_rutina

# Endpoints para gestión de series dentro de rutinas
@router.post("/{rutina_id}/series", response_model=SerieEjercicioResponse)
async def add_exercise_to_routine(
    rutina_id: int,
    serie: SerieEjercicioCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Agregar ejercicio a rutina"""
    # Verificar que la rutina existe y pertenece al usuario
    rutina = db.query(Rutina).filter(
        Rutina.id == rutina_id,
        Rutina.owner_id == current_user.id
    ).first()
    
    if not rutina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    # Verificar que el ejercicio existe
    ejercicio = db.query(Exercise).filter(Exercise.id == serie.ejercicio_id).first()
    if not ejercicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise not found"
        )
    
    db_serie = SerieEjercicio(**serie.dict(), rutina_id=rutina_id)
    db.add(db_serie)
    db.commit()
    db.refresh(db_serie)
    return db_serie

@router.put("/{rutina_id}/series/{serie_id}", response_model=SerieEjercicioResponse)
async def update_exercise_in_routine(
    rutina_id: int,
    serie_id: int,
    serie_update: SerieEjercicioUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar serie de ejercicio en rutina"""
    # Verificar permisos
    serie = db.query(SerieEjercicio).join(Rutina).filter(
        SerieEjercicio.id == serie_id,
        SerieEjercicio.rutina_id == rutina_id,
        Rutina.owner_id == current_user.id
    ).first()
    
    if not serie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise series not found"
        )
    
    update_data = serie_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(serie, field, value)
    
    db.commit()
    db.refresh(serie)
    return serie

@router.delete("/{rutina_id}/series/{serie_id}")
async def remove_exercise_from_routine(
    rutina_id: int,
    serie_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remover ejercicio de rutina"""
    # Verificar permisos
    serie = db.query(SerieEjercicio).join(Rutina).filter(
        SerieEjercicio.id == serie_id,
        SerieEjercicio.rutina_id == rutina_id,
        Rutina.owner_id == current_user.id
    ).first()
    
    if not serie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise series not found"
        )
    
    db.delete(serie)
    db.commit()
    return {"message": "Exercise removed from routine"}