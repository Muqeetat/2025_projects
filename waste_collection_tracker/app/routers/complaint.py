from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from .. import models
from ..models import Complaint, ComplaintUpdate, ComplaintCreate, User
from app.database import get_session
from datetime import date
from ..oauth2 import get_current_user, require_role
from sqlalchemy import and_

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

# Create a Complaint
@router.post("/", response_model=Complaint, response_model_exclude={"id", "updated_at"})
def create_complaint(complaint: ComplaintCreate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
   
    if current_user.id != complaint.resident_id:
        raise HTTPException(status_code=403, detail=f"Only the resident can make a complaint for themselves")
    
    # Populate complaint with the current user's data
    complaint.resident_id = current_user.id

    new_complaint = Complaint(**complaint.model_dump())
    session.add(new_complaint)
    session.commit()
    session.refresh(new_complaint)
    return new_complaint

# Combined endpoint to get Complaints by ID, location,date or all
@router.get("/", response_model=list[Complaint], response_model_exclude={"id","created_at", "updated_at"})
def get_complaint(
    complaint_id: int = None,
    location: str = None,
	start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Complaint)

	# Filter the query based on the parameters
    if complaint_id:
        query = query.filter(Complaint.id == complaint_id)
    if location:
        query = query.filter(Complaint.location == location)
    if start_date:
        query = query.filter(Complaint.created_at >= start_date)
    if end_date:
        query = query.filter(Complaint.created_at <= end_date)

    # Access control: Who can see what?
    if current_user.role == "resident":
        query = query.filter(Complaint.resident_id == current_user.id)  # Residents only see their complaints
    elif current_user.role == "admin" and current_user.id != 1:
        query = query.filter((Complaint.admin_id == current_user.id) | (Complaint.resident_id == current_user.id)) # Admins see relevant complaints
        
    complaints = session.exec(query.offset(skip).limit(limit)).all()

    if not complaints:
        raise HTTPException(status_code=404, detail="No matching complaints found")
    return complaints


# Update a complaint
@router.put("/{complaint_id}", response_model=Complaint, response_model_exclude={"id","created_at","updated_at"})
def update_complaint(complaint_id: int, complaint_data: ComplaintUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint with id {complaint_id} not found")

    if complaint.resident_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform action")

    # Update the complaint's attributes
    for field, value in complaint_data.dict(exclude_unset=True).items():
        setattr(complaint, field, value)
    session.commit()
    session.refresh(complaint)
    return complaint


# Delete a complaint
@router.delete("/{complaint_id}", response_model=Complaint)
def delete_complaint(complaint_id: int, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint.resident_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")

    session.delete(complaint)
    session.commit()
    return complaint

# Assign or reassign a complaint to an admin / Update a complaint
@router.put("/adminUpdate/")
def assign_admin(
    complaint_id: int, 
    admin_id: int = None,  # Optional: Only admin 1 can assign/reassign
    admin_update: str = None, 
    admin_response: str = None, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(require_role("admin"))
):
    # Fetch the pickup complaint
    complaint = session.exec(select(Complaint).where(Complaint.id == complaint_id)).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # If admin_id is provided, only admin 1 can assign/reassign
    if admin_id is not None:
        user = session.get(User, admin_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Admin with id {admin_id} not found")

        if user.role != "admin":
            raise HTTPException(status_code=400, detail="User is not an admin")
        
        if user.is_approved == False:
            raise HTTPException(status_code=400, detail="Admin account not approved")

        if complaint.admin_id == admin_id:
            raise HTTPException(status_code=400, detail=f"Complaint is already assigned to admin {admin_id}.")

        if current_user.id != 1:
            raise HTTPException(status_code=403, detail="Only admin 1 can assign or reassign complaints.")

        complaint.admin_id = admin_id  # Assign or reassign admin

    # If admin_update is provided, only the assigned admin can update it
    if admin_update or admin_response:
        if complaint.admin_id is None:
            raise HTTPException(status_code=403, detail="Complaint must be assigned to an admin before updating.")
        if complaint.admin_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only the assigned admin can update this complaint.")
        complaint.admin_update = admin_update
        complaint.admin_response = admin_response

    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    
    return complaint