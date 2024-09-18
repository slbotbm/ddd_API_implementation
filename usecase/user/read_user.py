from domain.user.user import User

def db_read_user(user_id: int, db):
    return db.query(User).filter(User.id == user_id).first()