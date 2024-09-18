from domain.task.task_status import TaskStatus

def db_complete_task(db_task, db):
    db_task.task_status = TaskStatus.complete
    db.commit()
    db.regresh(db_task)
    return True