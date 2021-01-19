from fastapi import APIRouter
from app.api.routes.users import router as user_router
from app.api.routes.profiles import router as profiles_router

router = APIRouter()

router.include_router(user_router, prefix='/users', tags=['users'])
router.include_router(profiles_router, prefix='/profiles', tags=['profiles'])
