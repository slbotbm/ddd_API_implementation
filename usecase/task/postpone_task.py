from dateutil.relativedelta import relativedelta
def db_postpone_task(db_task, db):
    db_task.delays += 1
    db_task.due_date += relativedelta(days=1)
    db.commit()
    db.refresh(db_task)