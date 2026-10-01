from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text())
    role: Mapped[str] = mapped_column(String(30), default="passenger")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Bus(Base):
    __tablename__ = "buses"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    plate_number: Mapped[str] = mapped_column(String(50), unique=True)
    capacity: Mapped[int] = mapped_column(default=40)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    route_id: Mapped[int | None] = mapped_column(
        ForeignKey("routes.id"),
        nullable=True,
        index=True,
    )

    route: Mapped["Route | None"] = relationship(
        "Route",
        back_populates="buses",
    )

class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    start_point: Mapped[str] = mapped_column(String(150))
    end_point: Mapped[str] = mapped_column(String(150))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    buses: Mapped[list["Bus"]] = relationship(
        "Bus",
        back_populates="route",
    )
    
class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(primary_key=True)
    bus_id: Mapped[int] = mapped_column(ForeignKey("buses.id"), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    speed_kmh: Mapped[float] = mapped_column(Float, default=0)
    heading: Mapped[float] = mapped_column(Float, default=0)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
