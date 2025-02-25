from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from .. import models
from ..models import PickupRequest, RequestUpdate, User, RequestCreate
from app.database import get_session
from datetime import date
from ..oauth2 import create_access_token, get_current_user, require_role
from sqlalchemy import and_


router = APIRouter(
    prefix="/pickup",
    tags=["Pickup Requests"]
)


# Create a PickupRequest
@router.post("/", response_model=PickupRequest, response_model_exclude={"id", "updated_at"})
def create_request(request: RequestCreate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):

    if request.location != current_user.location:
        raise HTTPException(status_code=403, detail=f"only residents in {current_user.location} can make a request")

    if current_user.id != request.resident_id:
        raise HTTPException(status_code=403, detail=f"Only the resident can make a request for themselves")
    
    if request.scheduled_date <= date.today():
        raise HTTPException(status_code=403, detail="Scheduled date must be in the future")

    if session.exec(select(PickupRequest).where(PickupRequest.scheduled_date == request.scheduled_date, 
        PickupRequest.resident_id == request.resident_id)).first():
        raise HTTPException(status_code=403, detail="A request has already been made for this date")

    # Populate request with the current user's data
    request.resident_id = current_user.id
    request.location = current_user.location

    new_request = PickupRequest(**request.model_dump())
    session.add(new_request)
    session.commit()
    session.refresh(new_request)
    return new_request


# Combined endpoint to get PickupRequests by ID, location, or all
@router.get("/", response_model=list[PickupRequest], response_model_exclude={"id","created_at", "updated_at"})
def get_pickup_requests(
    request_id: int = None,
    location: str = None,
    start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)    
):

    query = select(PickupRequest)

    if request_id:
        query = query.filter(PickupRequest.id == request_id)
    if location:
        query = query.filter(PickupRequest.location == location)
    if start_date:
        query = query.filter(PickupRequest.created_at >= start_date)
    if end_date:
        query = query.filter(PickupRequest.created_at <= end_date)
    
    if current_user.role == 'resident':
        query= query.filter(PickupRequest.resident_id == current_user.id)
        
    requests = session.exec(query.offset(skip).limit(limit)).all()

    if not requests:
        raise HTTPException(status_code=404, detail="No matching pickup requests found")

    return requests


# Update a PickupRequest       
@router.put("/{request_id}", response_model=PickupRequest, response_model_exclude={"id","created_at", "updated_at"})
def update_request(request_id: int, request_data: RequestUpdate, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):

    request = session.get(PickupRequest, request_id)
    if not request:
        raise HTTPException(status_code=404,  detail=f"Request with id {request_id} not found")

    if request.resident_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform action")

    if request_data.location and request_data.location != current_user.location:
        raise HTTPException(status_code=403, detail=f"only residents in {current_user.location} can make a request")

    if request_data.scheduled_date and request_data.scheduled_date <= date.today():
        raise HTTPException(status_code=403, detail="Scheduled date must be in the future")

    if session.exec(select(PickupRequest).where(PickupRequest.scheduled_date == request_data.scheduled_date, 
        PickupRequest.resident_id == current_user.id)).first():
        raise HTTPException(status_code=403, detail="A request has already been made for this date")

    # Update the request's attributes
    for field, value in request_data.dict(exclude_unset=True).items():
        setattr(request, field, value)
    session.commit()
    session.refresh(request)
    return request


# Delete a Pickup Request
@router.delete("/{request_id}", response_model=PickupRequest)
def delete_request(request_id: int, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    request = session.get(PickupRequest, request_id)

    if not request:
        raise HTTPException(status_code=404, detail=f"Request with id {request_id} not found")

    if request.resident_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform action")
    session.delete(request)
    session.commit()
    return request


@router.put("/adminUpdate/")
def approve_admin(
    request_id: int, 
    admin_id: int = None,  # Optional: Only admin 1 can assign/reassign
    admin_update: str = None, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(require_role("admin"))
):
    # Fetch the pickup request
    request = session.exec(select(PickupRequest).where(PickupRequest.id == request_id)).first()
    if not request:
        raise HTTPException(status_code=404, detail="Pickup request not found")

    # If admin_id is provided, only admin 1 can assign/reassign
    if admin_id is not None:
        user = session.get(User, admin_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {admin_id} not found")

        if request.admin_id == admin_id:
            raise HTTPException(status_code=400, detail="Request is already assigned to this admin.")

        if current_user.id != 1:
            raise HTTPException(status_code=403, detail="Only admin 1 can assign or reassign requests.")

        request.admin_id = admin_id  # Assign or reassign admin

    # If admin_update is provided, only the assigned admin (excluding Admin 1) can update it
    if admin_update:
        if request.admin_id is None:
            raise HTTPException(status_code=403, detail="Request must be assigned to an admin before updating.")
        if request.admin_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only the assigned admin can update this request.")
        request.admin_update = admin_update  

    session.add(request)
    session.commit()
    session.refresh(request)
    
    return request


