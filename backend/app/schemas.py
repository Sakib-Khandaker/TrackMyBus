from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str

class BusCreate(BaseModel):
    code: str
    plate_number: str
    capacity: int = Field(default=40, ge=1, le=200)

class BusOut(BusCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool

class BusOut(BaseModel):
    id: int
    code: str
    plate_number: str
    capacity: int
    is_active: bool
    route_id: int | None

    model_config = ConfigDict(from_attributes=True)

class BusRouteAssign(BaseModel):
    route_id: int | None = None

class RouteCreate(BaseModel):
    name: str
    start_point: str
    end_point: str

class RouteOut(RouteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool

class RouteBusOut(BaseModel):
    id: int
    code: str
    plate_number: str
    capacity: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class RouteDetailOut(RouteOut):
    buses: list[RouteBusOut] = []

class LocationCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    speed_kmh: float = Field(default=0, ge=0)
    heading: float = Field(default=0, ge=0, le=360)

class LocationOut(LocationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    bus_id: int
    recorded_at: datetime
