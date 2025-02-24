from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from .. import models
from ..models import Complaint, ComplaintUpdate
from app.database import get_session
from datetime import date


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

# Create a Complaint
@router.post("/", response_model=Complaint, response_model_exclude={"id", "updated_at"})
def create_complaint(complaint: Complaint, session: Session = Depends(get_session)):
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    return complaint

# python -m app.main

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

    complaints = session.exec(query.offset(skip).limit(limit)).all()

    if not complaints:
        raise HTTPException(status_code=404, detail="No matching complaints found")
    return complaints


# Update a complaint
@router.put("/{complaint_id}", response_model=Complaint, response_model_exclude={"id","created_at","updated_at"})
def update_complaint(complaint_id: int, complaint_data: Complaint, session: Session = Depends(get_session)):
    complaint = session.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="No matching complaints found")

    # Update the complaint's attributes
    for field, value in complaint_data.dict(exclude_unset=True).items():
        setattr(complaint, field, value)
    session.commit()
    session.refresh(complaint)
    return complaint


# # Delete a complaint
# @router.delete("/{complaint_id}", response_model=Complaint)
# def delete_complaint(complaint_id: int, session: Session = Depends(get_session)):
#     complaint = session.get(Complaint, complaint_id)
#     if not complaint:
#         raise HTTPException(status_code=404, detail="Complaint not found")

#     session.delete(complaint)
#     session.commit()
#     return complaint
