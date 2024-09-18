import schemas
from domain.task.task import Task

def db_create_task(task: schemas.TaskBase, db): 
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    return True