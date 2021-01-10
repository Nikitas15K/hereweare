from pydantic import BaseModel
from enum import Enum
from app.models.core import DateTimeModelMixin, IDModelMixin


class VehicleType(str, Enum):
    bicycle = "bicycle"
    motorcycle = "motorcycle"
    car = "car"
    truck = "truck"
    bus = "bus"


class Vehicles(BaseModel):
    """
    ...
    """
    sign: str
    type: VehicleType = "car"
    model: str
    manufacture_year: int


class VehiclesInDB(Vehicles, IDModelMixin):
    id: int
    sign: str
    type: VehicleType
    model: str
    manufacture_year: int


class VehiclesCreate(Vehicles):
    sign: str
    type: VehicleType
    model: str
    manufacture_year: int


class VehiclesPublic(Vehicles, IDModelMixin):
    pass
