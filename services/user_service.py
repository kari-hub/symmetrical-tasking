from models import User, Task
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserUpdate
from fastapi import status, HTTPException

"""
define the functions to create, get, update users    
"""


def create_new_user(db: Session, data: UserCreate):
    new_user = User(**data.model_dump())  # conversion to dict
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # delete associated tasks with user
    db.query(Task).filter(Task.owner_id == user_id).delete()

    db.delete(user)
    db.commit()
    return user

    """
    TODO: , current_id: User = Depends(), 403 FORBIDDEN for non-current users
    """
