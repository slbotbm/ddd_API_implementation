from domain.user.user import User

def db_read_users(db):
    return db.query(User).all()