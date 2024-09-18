from domain.task.task import Task

def db_read_task(task_id, db):
    return db.query(Task).filter(Task.id == task_id).first()