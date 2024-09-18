def db_delete_task(db_task, db):
    db.delete(db_task)
    db.commit()