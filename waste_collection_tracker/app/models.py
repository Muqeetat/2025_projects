from enum import Enum
from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime


# Define the Enums
class roles(str, Enum):
    admin = 'admin'
    resident = 'resident'

class locations(str, Enum):
    yaba = "yaba"
    surulere = "surulere"
    lekki = "lekki"

class admin_status(str, Enum):
    completed = 'completed'
    inprogress = 'in-progress'
    cancelled = 'cancelled'

class user_status(str, Enum):
    confirmed = 'confirmed'
    cancelled = 'cancelled'

# Define the Internal models
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: Optional[str] = None
    password: str
    location: locations
    role: roles
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

class PickupRequest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id : int
    scheduled_date: date
    admin_update:admin_status
    user_update: user_status
    location: locations
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    # admin_id : int

class Complaint(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int
    description: str
    status: admin_status
    admin_response: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    # admin_id: int

class UserCreate(SQLModel):
    name: str
    email: Optional[str] = None
    password: str
    location: str
    role: str = Field(default="resident") 
    
# Define the Response models
class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    location: Optional[str] = None

class RequestUpdate(SQLModel):
    scheduled_date: Optional[date] = None
    admin_update: Optional[str] = None
    user_update: Optional[str] = None
    location: Optional[str] = None
    # admin_id: Optional[int] = None
    
class ComplaintUpdate(SQLModel):
    description: Optional[str] = None
    status: Optional[str] = None
    admin_response: Optional[str] = None
    # admin_id: Optional[int] = None

class Token(SQLModel):
    access_token:str
    token_type:str
