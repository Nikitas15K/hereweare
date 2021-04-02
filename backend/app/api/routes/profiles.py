from fastapi import Depends, APIRouter, HTTPException, Path, Body, status
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.models.user import UserCreate, UserUpdate, UserInDB, UserPublic
from app.models.profile import ProfileUpdate, ProfilePublic
from app.db.repositories.profiles import ProfilesRepository
# from pydantic import EmailStr

router = APIRouter()


@router.get("/{user_id}/", response_model=ProfilePublic, name="profiles:get-profile-by-id")
async def get_profile_by_id(
    *, user_id: int,
    profile_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
) -> ProfilePublic:
    profile = await profile_repo.get_profile_by_user_id(user_id=user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such profile.")
    return profile
    


@router.put("/me/", response_model=ProfilePublic, name="profiles:update-own-profile")
async def update_own_profile(
    profile_update: ProfileUpdate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    profile_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
) -> ProfilePublic:
    updated_profile = await profile_repo.update_profile(profile_update=profile_update, requesting_user=current_user)
    return updated_profile
