from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from enums import TaskStatus
from dateutil.relativedelta import relativedelta
from enums import UserStatus

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/users/", status_code=status.HTTP_200_OK)
def read_users(db: db_dependency):
    users = db.query(models.User).all()

    if users == [] or users is None:
        raise HTTPException(status_code=404, detail="No users")
    return users


@app.get("/tasks/", status_code=status.HTTP_200_OK)
def read_tasks(db: db_dependency):
    tasks = db.query(models.Task).all()

    if tasks == [] or tasks is None:
        raise HTTPException(status_code=404, detail="No tasks")
    return tasks


@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}


@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskBase, db: db_dependency):
    owner = db.query(models.User).filter(models.User.id == task.owner_id).first()

    if owner is None:
        raise HTTPException(
            status_code=400, detail="Invalid owner_id. User does not exist."
        )
    if owner.user_status != UserStatus.active:
        raise HTTPException(
            status_code=400, detail="Please choose an owner who is active."
        )

    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    return {"message": "Task created successfully"}


@app.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserResponse,
)
def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/tasks/{user_id}", status_code=status.HTTP_200_OK)
def read_task(task_id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: schemas.UserUpdate, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: schemas.TaskUpdate, db: db_dependency):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return {"message": "Task updated successfully"}


@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: db_dependency):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


@app.put("/tasks/{task_id}/delay", status_code=status.HTTP_200_OK)
def delay(task_id: int, db: db_dependency):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.task_status == TaskStatus.complete:
        raise HTTPException(status_code=400, detail="Task is complete")
    if db_task.delays > 3:
        raise HTTPException(status_code=400, detail="Cannot delay task any further.")

    db_task.delays += 1
    db_task.due_date += relativedelta(days=1)
    db.commit()
    db.refresh(db_task)

    return {"message": "Task successfully delayed"}
