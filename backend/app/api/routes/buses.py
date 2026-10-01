from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_role
from app.models import Bus, Route
from app.schemas import BusCreate, BusOut
from app.schemas import BusCreate, BusOut, BusRouteAssign

router = APIRouter()


@router.get("", response_model=list[BusOut])
def list_buses(db: Session = Depends(get_db)):
    return list(db.scalars(select(Bus).order_by(Bus.id)))


@router.get("/{bus_id}", response_model=BusOut)
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db),
):
    bus = db.get(Bus, bus_id)

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    return bus


@router.post("", response_model=BusOut, status_code=201)
def create_bus(
    data: BusCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    bus = Bus(
        code=data.code.strip(),
        plate_number=data.plate_number.strip(),
        capacity=data.capacity,
    )

    db.add(bus)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Bus code or plate number already exists",
        )

    db.refresh(bus)
    return bus


@router.put("/{bus_id}", response_model=BusOut)
def update_bus(
    bus_id: int,
    data: BusCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    bus = db.get(Bus, bus_id)

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    bus.code = data.code.strip()
    bus.plate_number = data.plate_number.strip()
    bus.capacity = data.capacity

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Bus code or plate number already exists",
        )

    db.refresh(bus)
    return bus


@router.delete("/{bus_id}", status_code=204)
def delete_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    bus = db.get(Bus, bus_id)

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    bus.is_active = False
    db.commit()


@router.patch("/{bus_id}/route", response_model=BusOut)
def assign_route(
    bus_id: int,
    data: BusRouteAssign,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    bus = db.get(Bus, bus_id)

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found",
        )

    if data.route_id is not None:
        route = db.get(Route, data.route_id)

        if not route:
            raise HTTPException(
                status_code=404,
                detail="Route not found",
            )

        if not route.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign bus to an inactive route",
            )

    bus.route_id = data.route_id

    db.commit()
    db.refresh(bus)

    return bus