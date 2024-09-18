from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from database import Base
from enums import TaskStatus, UserStatus


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    task_status = Column(Enum(TaskStatus))
    owner_id = Column(Integer, ForeignKey("users.id"))
    due_date = Column(DateTime)
    delays = Column(Integer)

    owner = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_status = Column(Enum(UserStatus))
    email = Column(String, unique=True, index=True)
    phone = Column(Integer, unique=True, index=True)

    tasks = relationship("Task", back_populates="owner")
