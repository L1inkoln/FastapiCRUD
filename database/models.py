from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


# Базовый класс для декларативной модели
class Base(DeclarativeBase):
    pass


# Создаем таблицу с использованием ORM
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
