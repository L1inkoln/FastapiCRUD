from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from core.exceptions import AlreadyExistsException, NotFoundException
from services.user_service import UserService
from schemas.user import UserCreate, UserResponse, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.create_user(user)
    except AlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return UserService(db).get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return UserService(db).get_user_by_id(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/usernames/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    try:
        return UserService(db).get_user_by_username(username)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        return UserService(db).update_user(user_id, user_update)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        UserService(db).delete_user(user_id)
        return {"status": "success", "message": f"User with id {user_id} deleted"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
