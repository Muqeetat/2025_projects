from fastapi import APIRouter, Depends, HTTPException
from ..database import get_session
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User,UserCreate,UserLogin
from ..utils import get_password_hash, verify_password
from ..oauth2 import create_access_token, get_current_user, require_role


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup") #,response_model=User, response_model_exclude={"id", "updated_at"})
def resident_signup(user:UserCreate,session: Session = Depends(get_session)):
    # Check if the username is already taken
    if session.exec(select(User).where(User.name == user.name)).first():
        raise HTTPException(status_code=400, detail="Username already Exists")
    # Create a new user with default role 'resident'
    
    user.password = get_password_hash(user.password)

    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": f"Resident account created successfully for {user.name}"}
    # return user 


@router.post("/resident/login")
def resident_login(user_credential: OAuth2PasswordRequestForm=Depends(), session: Session = Depends(get_session)):
    if not user_credential.username or not user_credential.password:
        raise HTTPException(status_code=422, detail="Username and password must be provided")

    user = session.exec(select(User).where(User.name == user_credential.username)).first()
    if not user or not verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if user.role != "resident":
        raise HTTPException(status_code=403, detail="Only residents can log in via this route.")

    access_token = create_access_token(data={"name": user.name, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer","msg": f"Login successful. Welcome {user.name}!" }



@router.post("/admin/signup")
def admin_signup(user_data: UserCreate, session: Session = Depends(get_session)):
    
    if session.exec(select(User).where(User.name == user_data.name)).first():
        raise HTTPException(status_code=400, detail="Username already exists.")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        location=user_data.location,
        role="admin"
        )
        
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    # return new_user
    return {"msg": f"Admin account created successfully for {user_data.name}"}

@router.post("/login")
def admin_login(credentials: OAuth2PasswordRequestForm=Depends(), session: Session = Depends(get_session)):
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=422, detail="Username and password must be provided")

    user = session.exec(select(User).where(User.name == credentials.username)).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can log in via this route.")

    if not user.is_approved:
        raise HTTPException(status_code=403, detail="Admin account not approved.")

    token = create_access_token(data={"name": user.name, "role": user.role})
    return {"access_token": token, "token_type": "bearer","msg": f"Login successful. Welcome {user.name}!"}



@router.put("/approve/{user_id}")
def approve_admin(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(require_role("admin"))):
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User with id {user_id} not found")

    if user.role != "admin":
        raise HTTPException(status_code=400, detail="User is not an admin")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Admin cannot approve self")

    if user.is_approved:
        raise HTTPException(status_code=400, detail="Admin already approved")

    if current_user.id != 1:
        raise HTTPException(status_code=403, detail="Only admin 1 can approve admins")

    user.is_approved = True
    session.add(user)
    session.commit()
    return {"msg": f"Admin {user.name} approved successfully."}