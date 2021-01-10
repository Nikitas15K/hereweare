from pydantic import BaseModel, EmailStr
from app.models.core import DateTimeModelMixin, IDModelMixin


class InsuranceCompany(BaseModel):
    """
    ...
    """
    name: str
    email: EmailStr


class InsuranceCompanyInDB(InsuranceCompany, IDModelMixin):
    id: int
    name: str
    email: EmailStr


class InsuranceCompanyCreate(InsuranceCompany):
    name: str
    email: EmailStr


class InsuranceCompanyPublic(InsuranceCompany, IDModelMixin):
    pass
