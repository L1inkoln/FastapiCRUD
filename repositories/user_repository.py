from typing import List, Optional
from sqlalchemy.orm import Session
from database.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Получить пользователя по username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self) -> List[User]:
        """Получить всех пользователей"""
        return self.db.query(User).all()

    def create(self, user: User) -> User:
        """Создать нового пользователя"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, update_data: dict) -> Optional[User]:
        """Обновить данные пользователя"""
        db_user = self.get_by_id(user_id)
        if db_user:
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        """Удалить пользователя"""
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
