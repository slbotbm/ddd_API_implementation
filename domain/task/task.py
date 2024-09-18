from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from domain.shared import database
from domain.task.task_status import TaskStatus

class Task(database.Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    task_status = Column(Enum(TaskStatus))
    owner_id = Column(Integer, ForeignKey("users.id"))
    due_date = Column(DateTime)
    delays = Column(Integer)

    owner = relationship("User", back_populates="tasks")