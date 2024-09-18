from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from domain.shared import database
from domain.user.user_status import UserStatus


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_status = Column(Enum(UserStatus))
    email = Column(String, unique=True, index=True)
    phone = Column(Integer, unique=True, index=True)

    tasks = relationship("Task", back_populates="owner")
