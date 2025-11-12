from services.user_service import (
    create_new_user,
    get_all_users,
    get_user_by_email,
    get_user,
    update_user,
    delete_user,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from schemas.users import UserCreate, UserUpdate, User
from services.auth import get_current_user
from typing import List


router = APIRouter(tags=["User APIs"])


@router.post(
    "/register",
    response_model=User,
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists!")
    user = create_new_user(db, user_in)
    return user


@router.get("/user/{user_id}", response_model=User, description="Fetch a single user")
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)  # correct parameter order
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[User], description="Get all existing users")
async def list_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users


@router.patch(
    "/user/{user_id}", response_model=User, description="Update a user's details"
)
def patch_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # allow only owner to change their profile
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    updated = update_user(db, user_id, user_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated


@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a user",
)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # only allow users to delete their own accounts
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete other users",
        )
    delete_user(db, user_id)
    return None  # 204 no content does not need a response body
