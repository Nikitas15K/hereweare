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
from app.models.user import UserPublic, UserUpdate, UserInDB
from app.db.repositories.admin import AdminRepository
from app.db.repositories.users import UsersRepository
from app.api.dependencies.auth import get_current_active_user


router = APIRouter()

@router.get("/", response_model= List[dict], name="users:get-all-users")
async def get_all_users(
    current_user: UserPublic = Depends(get_current_active_user),
    admin_repo: AdminRepository = Depends(get_repository(AdminRepository)),
)  -> List[dict]:
    if current_user.is_master == True:
        return await admin_repo.get_all_users()
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do not have access.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/activate_not/{id}", response_model=UserPublic, name="users:block-activate-user")
async def block_activate_user(id:int,
        current_user: UserInDB = Depends(get_current_active_user),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
)-> UserPublic:
    if current_user.is_master:
        return await users_repo.block_unblock_user(id= id)
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No access")

@router.put("/superuser/{id}", response_model=UserPublic, name="users:superuser")
async def superuser(id:int,
        current_user: UserInDB = Depends(get_current_active_user),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
)-> UserPublic:
    if current_user.is_master:
        return await users_repo.superuser(id= id)
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No access")

@router.get("/search", response_model= List[dict], name="users:get-search")
async def get_search(username:str,
    current_user: UserPublic = Depends(get_current_active_user),
    admin_repo: AdminRepository = Depends(get_repository(AdminRepository)),
)  -> List[dict]:
    if current_user.is_master == True:
        return await admin_repo.get_search(username=username)
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do not have access.",
            headers={"WWW-Authenticate": "Bearer"},
        )