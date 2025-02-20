from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select
from .. import models
from ..models import PickupRequest, RequestUpdate
from app.database import get_session
from datetime import date



router = APIRouter(
    prefix="/pickup",
    tags=["Pickup Requests"]
)


# Create a PickupRequest
@router.post("/", response_model=PickupRequest, response_model_exclude={"id", "updated_at"})
def create_request(request: PickupRequest, session: Session = Depends(get_session)):
    session.add(request)
    session.commit()
    session.refresh(request)
    return request



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
    
    requests = session.exec(query.offset(skip).limit(limit)).all()

    if not requests:
        raise HTTPException(status_code=404, detail="No matching pickup requests found")
    return requests



# Update a PickupRequest        the admin can only update the admin_status , resident can only make update to the user_staus.  
# Location has to be the same as the user.locations else error message "update ur location in user profile" 
@router.put("/{request_id}", response_model=PickupRequest, response_model_exclude={"id","created_at", "updated_at"})
def update_request(request_id: int, request_data: RequestUpdate, session: Session = Depends(get_session)):
    request = session.get(PickupRequest, request_id)
    if not request:
        raise HTTPException(status_code=404,  detail=f"Request with id {request_id} not found")

    # Update the request's attributes
    for field, value in request_data.dict(exclude_unset=True).items():
        setattr(request, field, value)
    session.commit()
    session.refresh(request)
    return request



# # Delete a Pickup Request
# @router.delete("/{request_id}", response_model=PickupRequest)
# def delete_request(request_id: int, session: Session = Depends(get_session)):
#     request = session.get(PickupRequest, request_id)
#     if not request:
#         raise HTTPException(status_code=404, detail=f"")

#     session.delete(request)
#     session.commit()
#     return request