from fastapi import APIRouter, Depends, HTTPException
from ..database import get_session
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User,UserCreate ,Token
from ..utils import get_password_hash, verify_password
from ..oauth2 import create_access_token, get_current_user, require_role


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup") #,response_model=User, response_model_exclude={"id", "updated_at"})
def signup(user:UserCreate,session: Session = Depends(get_session)):

    if session.exec(select(User).where(User.name == user.name)).first():
        raise HTTPException(status_code=400, detail="Username already Exists")
    user = User(name=user.name, email = user.email, password=get_password_hash(user.password),location = user.location, role=user.role)
    session.add(user)
    session.commit()
    return {"msg": "User created successfully"}
    # session.refresh(user)
    # return user 

@router.post("/login", response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    if not user_credential.username or not user_credential.password:
        raise HTTPException(status_code=422, detail="Username and password must be provided")
    user = session.exec(select(User).where(User.name == user_credential.username)).first()
    if not user or not verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"name": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user.username}! Your role is {current_user.role}."}

@router.get("/admin-only")
def admin_route(current_user: User = Depends(require_role("admin"))):
    return {"msg": f"Welcome Admin {current_user.username}! You have special access."}