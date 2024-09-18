def db_update_user(user, db_user, db):
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return True