from domain.task.task import Task

def db_read_tasks(db):
    return db.query(Task).all()