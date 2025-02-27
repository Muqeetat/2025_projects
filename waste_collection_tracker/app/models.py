from enum import Enum
from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy import Column, Enum as SQLAEnum, DateTime


# Define Enums
class Roles(str, Enum):
    admin = 'admin'
    resident = 'resident'

class Locations(str, Enum):
    yaba = "yaba"
    surulere = "surulere"
    lekki = "lekki"

class ResidentStatus(str, Enum):
    inprogress = 'in-progress'
    confirmed = "confirmed"
    cancelled = "cancelled"

class AdminStatus(str, Enum):
    completed = 'completed'
    inprogress = 'in-progress'
    cancelled = 'cancelled'

# Authentication Models
class UserLogin(SQLModel):
    name: str
    password: str

class UserCreate(UserLogin):
    email: Optional[str] = None
    location: Locations 

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    location: Optional[Locations] = None

class RequestCreate(SQLModel):
    resident_id: int
    location: Locations
    scheduled_date: date

class RequestUpdate(SQLModel):
    scheduled_date: Optional[date] = None
    resident_update: Optional[str] = None
    location: Optional[Locations] = None

class ComplaintCreate(SQLModel):
    resident_id :int
    description: str

class ComplaintUpdate(SQLModel):
    description: Optional[str] = None
    resident_update: Optional[str] = None

# User Model
class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True, nullable=False)
    email: Optional[str] = None
    password: str
    location: Locations = Field(sa_column=Column(SQLAEnum(Locations)))
    role: Roles = Field(default=Roles.resident, sa_column=Column(SQLAEnum(Roles)))
    is_approved: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    pickup_requests: List["PickupRequest"] = Relationship(back_populates="user", sa_relationship_kwargs={"foreign_keys": "PickupRequest.resident_id"})
    assigned_pickups: List["PickupRequest"] = Relationship(
        back_populates="assigned_admin", sa_relationship_kwargs={"foreign_keys": "PickupRequest.admin_id"}
    )

    complaints: List["Complaint"] = Relationship(back_populates="user" , sa_relationship_kwargs={"foreign_keys": "Complaint.resident_id"})
    assigned_complaints: List["Complaint"] = Relationship(
        back_populates="assigned_admin", sa_relationship_kwargs={"foreign_keys": "Complaint.admin_id"}
    )

# Pickup Request Model
class PickupRequest(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    resident_id: int = Field(foreign_key="user.id", nullable=False)
    resident_update: Optional[ResidentStatus] = Field(sa_column=Column(SQLAEnum(ResidentStatus)))
    scheduled_date: date
    location: Locations = Field(sa_column=Column(SQLAEnum(Locations)))
    admin_id: Optional[int] = Field(foreign_key="user.id", nullable=True)
    admin_update: Optional[AdminStatus] = Field(sa_column=Column(SQLAEnum(AdminStatus)))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    user: User = Relationship(back_populates="pickup_requests", sa_relationship_kwargs={"foreign_keys": "PickupRequest.resident_id"})
    assigned_admin: Optional[User] = Relationship(
        back_populates="assigned_pickups", sa_relationship_kwargs={"foreign_keys": "PickupRequest.admin_id"}
    )

# Complaint Model
class Complaint(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    resident_id: int = Field(foreign_key="user.id", nullable=False)
    resident_update: Optional[ResidentStatus] = Field(sa_column=Column(SQLAEnum(ResidentStatus)))
    description: str
    admin_id: Optional[int] = Field(foreign_key="user.id", nullable=True)
    admin_update: Optional[AdminStatus] = Field(sa_column=Column(SQLAEnum(AdminStatus)))
    admin_response: Optional[str] = None 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

    user: User = Relationship(back_populates="complaints" , sa_relationship_kwargs={"foreign_keys": "Complaint.resident_id"})
    assigned_admin: Optional[User] = Relationship(
        back_populates="assigned_complaints", sa_relationship_kwargs={"foreign_keys": "Complaint.admin_id"}
    )
