from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from .. import models
from ..models import User, UserUpdate
from app.database import get_session


router = APIRouter(
	prefix="/users",
	tags=["Users"]
)

# Tasks
# only admin can get user by id
# users can only update their own details



# Get a user by ID
@router.get("/{user_id}", response_model=User, response_model_exclude={"id","created_at", "updated_at"})
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user

# the user update their details
@router.put("/{user_id}", response_model=User, response_model_exclude={"id","created_at","updated_at"})
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404,  detail=f"User with id {user_id} not found")

    # Update the user's attributes
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user