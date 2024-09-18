from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

import schemas
from domain.shared import database

# Domain
from domain.user.user_status import UserStatus
from domain.task.task_status import TaskStatus

# Usecase
from domain.shared.database import engine, SessionLocal
from usecase.user.read_users import db_read_users
from usecase.user.create_user import db_create_user
from usecase.user.read_user import db_read_user
# from usecase.user.delete_user import db_delete_user
# from usecase.user.update_user import db_update_user
from usecase.user.deactivate_user import db_deactivate_user
from usecase.task.read_tasks import db_read_tasks
from usecase.task.create_task import db_create_task
from usecase.task.read_tasks import db_read_tasks
from usecase.task.read_task import db_read_task
# from usecase.task.delete_task import db_delete_task
# from usecase.task.update_task import db_update_task
from usecase.task.postpone_task import db_postpone_task
from usecase.task.complete_task import db_complete_task

database.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return "OK"

@app.get("/users/", status_code=status.HTTP_200_OK)
def read_users(db: db_dependency):
    users = db_read_users(db)

    if users == [] or users is None:
        raise HTTPException(status_code=404, detail="No users")
    return users


@app.get("/tasks/", status_code=status.HTTP_200_OK)
def read_tasks(db: db_dependency):
    tasks = db_read_tasks(db)

    if tasks == [] or tasks is None:
        raise HTTPException(status_code=404, detail="No tasks")
    return tasks


@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserBase, db: db_dependency):
    try:
        result = db_create_user(user, db)
        if result:
            return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskBase, db: db_dependency):
    owner = db_read_user(task.owner_id, db)

    if owner is None:
        raise HTTPException(
            status_code=400, detail="Invalid owner_id. User does not exist."
        )
    if owner.user_status != UserStatus.active:
        raise HTTPException(
            status_code=400, detail="Please choose an owner who is active."
        )

    try:
        result = db_create_task(task, db)
        if result:
            return {"message": "Task created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@app.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserResponse,
)
def read_user(user_id: int, db: db_dependency):
    user = db_read_user(user_id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/tasks/{user_id}", status_code=status.HTTP_200_OK)
def read_task(task_id: int, db: db_dependency):
    task = db_read_task(task_id, db)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# @app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
# def update_user(user_id: int, user: schemas.UserUpdate, db: db_dependency):
#     db_user = db_read_user(user_id, db)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     try:
#         result = db_update_user(user, db_user, db)
#         if result:
#             return {"message": "User updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error: {e}")

# @app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
# def delete_user(user_id: int, db: db_dependency):
#     db_user = db_read_user(user_id, db)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     try:
#         result = db_delete_user(db_user, db)
#         if result:
#             return {"message": "User deleted successfully"}
#     except Exception as e: 
#         raise HTTPException(status_code=400, detail=f"Error: {e}")


# @app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
# def update_task(task_id: int, task: schemas.TaskUpdate, db: db_dependency):
#     db_task = db_read_task(task_id, db)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     try:
#         result = db_update_task(db_task, task, db)
#         if result:
#             return {"message": "Task updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error: {e}")


# @app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
# def delete_task(task_id: int, db: db_dependency):
#     db_task = db_read_task(task_id, db)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     try:
#         result = db_delete_task(db_task, db)
#         if result:
#             return {"message": "Task deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error: {e}")


@app.put("/tasks/{task_id}/postpone", status_code=status.HTTP_200_OK)
def postpone_task(task_id: int, db: db_dependency):
    db_task = db_read_task(task_id, db)

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.task_status == TaskStatus.complete:
        raise HTTPException(status_code=400, detail="Task is complete")
    if db_task.delays > 3:
        raise HTTPException(status_code=400, detail="Cannot delay task any further.")

    try:
        result = db_postpone_task(db_task, db)
        if result:
            return {"message": "Task successfully delayed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")

@app.put("/user/{user_id}/deactivate", status_code=status.HTTP_200_OK)
def deactivate_user(user_id: int, db: db_dependency):
    db_user = db_read_user(user_id, db)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        result = db_deactivate_user(db_user, db)
        if result:
            return {"Message": "User deactivated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    

@app.put("/task/{user_id}/complete", status_code=status.HTTP_200_OK)
def complete_task(task_id: int, db: db_dependency):
    db_task = db_read_task(task_id, db)

    if db_task is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        result = db_complete_task(db_task, db)
        if result:
            return {"Message": "Task completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")