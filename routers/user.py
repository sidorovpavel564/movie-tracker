from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services import user as UserService
from dto import user as UserDTO
from response_model import user as UserResponseModel

router = APIRouter()


@router.post('/', tags=["user"], response_model=List[UserResponseModel.User])
async def create(data: UserDTO.User = None, db: Session = Depends(get_db)):
    return UserService.create_user(data, db)


@router.get('/{id}', tags=["user"], response_model=List[UserResponseModel.User])
async def get(id: int = None, db: Session = Depends(get_db)):
    return UserService.get_user(id, db)


@router.put('/{id}', tags=["user"], response_model=List[UserResponseModel.User])
async def update(id: int = None, data: UserDTO.User = None,  db: Session = Depends(get_db)):
    return UserService.update(data, db, id)


@router.delete('/{id}', tags=["user"], response_model=List[UserResponseModel.User])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return UserService.remove(db, id)
