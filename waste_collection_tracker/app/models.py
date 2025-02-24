from enum import Enum
from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship, Column


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


class UserLogin(SQLModel):
    name: str
    password: str

class UserCreate(UserLogin):
    email: Optional[str] = None
    location: str

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

# Define the Internal models
class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True, nullable=False)
    email: Optional[str] = None
    password: str
    location: locations
    role: roles = Field(default="resident")
    is_approved: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    pickup_requests: List["PickupRequest"] = Relationship(back_populates="user")      # Shows which pickup requests this user has made.
    assigned_pickups: List["PickupRequest"] = Relationship(back_populates="assigned_admin", sa_relationship_kwargs={"foreign_keys": "[PickupRequest.admin_id]"})

    complaints: List["Complaint"] = Relationship(back_populates="user")      # Shows which complaints this user has made.
    assigned_complaints: List["Complaint"] = Relationship(back_populates="assigned_admin", sa_relationship_kwargs={"foreign_keys": "[Complaint.admin_id]"})

class PickupRequest(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    resident_id : int = Field(foreign_key="user.id", nullable=False)
    resident_update: Optional[user_status] = Field(default=None, sa_column=Column(Enum(user_status)))
    scheduled_date: date
    location: locations
    admin_id :  Optional[int] = Field(foreign_key="user.id", nullable=True)  # Assigned admin
    admin_update:Optional[admin_status] = Field(default=None, sa_column=Column(Enum(admin_status)))
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    user: User = Relationship(back_populates="pickup_requests")
    assigned_admin: Optional[User] = Relationship(back_populates="assigned_pickups", sa_relationship_kwargs={"foreign_keys": "[PickupRequest.admin_id]"})


class Complaint(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    resident_id: int = Field(foreign_key="user.id", nullable=False)
    resident_update: Optional[user_status] = Field(default=None, sa_column=Column(Enum(user_status)))
    description: str
    admin_id: Optional[int] = Field(foreign_key="user.id", nullable=True)  # Assigned admin
    admin_update: Optional[admin_status] = Field(default=None, sa_column=Column(Enum(admin_status)))
    admin_response: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    user: User = Relationship(back_populates="complaints")
    assigned_admin: Optional[User] = Relationship(back_populates="assigned_complaints", sa_relationship_kwargs={"foreign_keys": "[Complaint.admin_id]"})
