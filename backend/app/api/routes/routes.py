from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_role
from app.models import Route
from app.schemas import (
    RouteCreate,
    RouteOut,
    RouteDetailOut,
)

router = APIRouter()


@router.get("", response_model=list[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    return list(db.scalars(select(Route).order_by(Route.id)))


@router.get("/{route_id}", response_model=RouteDetailOut)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
):
    route = db.get(Route, route_id)

    if not route:
        raise HTTPException(
            status_code=404,
            detail="Route not found",
        )

    return route


@router.post("", response_model=RouteOut, status_code=201)
def create_route(
    data: RouteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    route = Route(**data.model_dump())

    db.add(route)
    db.commit()
    db.refresh(route)

    return route


@router.put("/{route_id}", response_model=RouteOut)
def update_route(
    route_id: int,
    data: RouteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    route = db.get(Route, route_id)

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    route.name = data.name
    route.start_point = data.start_point
    route.end_point = data.end_point

    db.commit()
    db.refresh(route)

    return route


@router.delete("/{route_id}", status_code=204)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    route = db.get(Route, route_id)

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    route.is_active = False
    db.commit()