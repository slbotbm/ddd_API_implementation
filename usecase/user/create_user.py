import schemas
from domain.user.user import User

def db_create_user(user: schemas.UserBase, db): 
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return True