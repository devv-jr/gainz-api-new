"""
Router para gestión de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, UserUpdate, UserResponse
from routers.auth import get_current_active_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """Obtener perfil del usuario actual"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar perfil del usuario actual"""
    update_data = user_update.dict(exclude_unset=True)
    
    # Verificar si el email ya existe (si se está actualizando)
    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Verificar si el username ya existe (si se está actualizando)
    if "username" in update_data:
        existing_user = db.query(User).filter(
            User.username == update_data["username"],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Actualizar campos
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/profile")
async def delete_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Eliminar cuenta del usuario actual"""
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}