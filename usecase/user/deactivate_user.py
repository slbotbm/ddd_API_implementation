from domain.user.user_status import UserStatus

def db_deactivate_user(db_user, db):
    db_user.user_status = UserStatus.inactive
    db.commit()
    db.refresh(db_user)
    return True