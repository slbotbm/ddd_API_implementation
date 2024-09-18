def db_update_task(db_task, task, db):
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)