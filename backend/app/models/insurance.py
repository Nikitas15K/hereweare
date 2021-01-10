from pydantic import BaseModel
from app.models.core import DateTimeModelMixin, IDModelMixin

class Insurance(BaseModel):
    """
    ...
    """
    number: str
    expire_date: int
    vehicle_id: int
    insurance_company_id: int


class InsuranceAdd(Insurance):
    number: str
    expire_date: int
    vehicle_id: int
    insurance_company_id: int


class InsuranceInDB(IDModelMixin, Insurance):
    id: int
    number: str
    expire_date: int
    vehicle_id: int
    insurance_company_id: int


class InsurancePublic(IDModelMixin, Insurance):
    pass
