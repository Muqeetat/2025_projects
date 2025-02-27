from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from .. import models
from ..models import User, UserUpdate
from app.database import get_session
from ..utils import get_password_hash
from ..oauth2 import get_current_user, require_role
from datetime import date


router = APIRouter(
	prefix="/users",
	tags=["Users"]
)


@router.get("/", response_model=list[User], response_model_exclude={"id","password","is_approved","updated_at"})
def get_user(
    user_id: int = None,
    location: str = None,
	start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role("admin"))
):
    query = select(User)

	# Filter the query based on the parameters
    if user_id:
        query = query.filter(User.id == user_id)
    if location:
        query = query.filter(User.location == location)
    if start_date:
        query = query.filter(User.created_at >= start_date)
    if end_date:
        query = query.filter(User.created_at <= end_date)

    users = session.exec(query.offset(skip).limit(limit)).all()

    if current_user.id != 1:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")
    if not users:
        raise HTTPException(status_code=404, detail="No matching users found")
    return users


# Get a user by name
@router.get("/{username}", response_model=User, response_model_exclude={"password","is_approved","created_at", "updated_at"})
def get_username(username: str, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    user = session.exec(select(User).where(User.name == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {username} not found")
    
    if user.name != current_user.name:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform action")
    return user


# the user update their details
@router.put("/{user_id}", response_model=User, response_model_exclude={"id","is_approved","created_at","updated_at"})
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404,  detail=f"User with id {user_id} not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform action")

    if user_data.password is not None:
        user_data.password = get_password_hash(user_data.password)
    # Update the user's attributes
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user