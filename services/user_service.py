from typing import List, Optional
from sqlalchemy.orm import Session
from core.security import hash_password, verify_password
from database.models import User
from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate
from core.exceptions import NotFoundException, AlreadyExistsException


class UserService:
    def __init__(self, db_session: Session):
        self.repository = UserRepository(db_session)

    def create_user(self, user_create: UserCreate) -> User:
        """Создание пользователя с хешированием пароля."""
        if self.repository.get_by_username(user_create.username):
            raise AlreadyExistsException("Username already taken")

        hashed_password = hash_password(user_create.password)
        user = User(
            name=user_create.name,
            age=user_create.age,
            username=user_create.username,
            password=hashed_password,
        )
        return self.repository.create(user)

    def get_all_users(self) -> List[User]:
        """Получение всех пользователей (ORM-модели)"""
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID."""
        if user := self.repository.get_by_id(user_id):
            return user
        raise NotFoundException("User not found")

    def get_user_by_username(self, username: str) -> User:
        """Получение пользователя по username."""
        if user := self.repository.get_by_username(username):
            return user
        raise NotFoundException("User not found")

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Обновление данных пользователя."""
        update_data = user_update.model_dump(exclude_unset=True)
        if not (user := self.repository.update(user_id, update_data)):
            raise NotFoundException("User not found")
        return user

    def delete_user(self, user_id: int) -> None:
        """Удаление пользователя (без возврата данных)"""
        if not self.repository.delete(user_id):
            raise NotFoundException("User not found")

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        if user := self.repository.get_by_username(username):
            if verify_password(password, user.password):
                return user
        return None
