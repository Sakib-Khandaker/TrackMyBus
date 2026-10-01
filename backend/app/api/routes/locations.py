from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.deps import require_role
from app.models import Bus, Location
from app.schemas import LocationCreate, LocationOut

router = APIRouter()

@router.post("/{bus_id}/location", response_model=LocationOut, status_code=201)
def add_location(
    bus_id: int,
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("driver", "admin")),
):
    bus = db.get(Bus, bus_id)
    if not bus:
        raise HTTPException(404, "Bus not found")
    location = Location(bus_id=bus_id, **data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

@router.get("/{bus_id}/location", response_model=LocationOut)
def latest_location(bus_id: int, db: Session = Depends(get_db)):
    location = db.scalar(
        select(Location)
        .where(Location.bus_id == bus_id)
        .order_by(Location.recorded_at.desc())
        .limit(1)
    )
    if not location:
        raise HTTPException(404, "No location recorded")
    return location
