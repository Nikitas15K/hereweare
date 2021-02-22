from fastapi import Depends, APIRouter, HTTPException, Path, Body
from typing import List
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from app.api.dependencies.database import get_repository
from app.models.user import UserPublic, UserUpdate
from app.db.repositories.admin import AdminRepository
from app.api.dependencies.auth import get_current_active_user


router = APIRouter()

@router.get("/", response_model= List[dict], name="users:get-all-users")
async def get_all_users(
    current_user: UserPublic = Depends(get_current_active_user),
    admin_repo: AdminRepository = Depends(get_repository(AdminRepository)),
)  -> List[dict]:
    if current_user.is_superuser == True:
        return await admin_repo.get_all_users()
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do not have access.",
            headers={"WWW-Authenticate": "Bearer"},
        )
