def db_delete_user(db_user, db):
    db.delete(db_user)
    db.commit()
    return True