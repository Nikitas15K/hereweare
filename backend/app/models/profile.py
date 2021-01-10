from typing import Optional
from pydantic import EmailStr, constr, HttpUrl, BaseModel
from app.models.core import DateTimeModelMixin,IDModelMixin


class ProfileBase(BaseModel):
    """
    Leaving off password and salt from base model
    """
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[constr(regex="^\d{1,3}-\d{1,3}?-\d{1,4}?$")]
    licence_number: Optional[str]
    licence_category: Optional[str]
    licence_expire_date: Optional[int]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):

    user_id: int


class ProfileUpdate(ProfileBase):
    """
    Allow users to update any or no fields, as long as it's not user_id
    """
    pass


class ProfileInDB(IDModelMixin, DateTimeModelMixin, ProfileBase):
    user_id: int
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    pass


