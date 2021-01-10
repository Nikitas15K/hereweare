from fastapi import APIRouter
from app.api.routes.vehicles import router as vehicles_router
from app.api.routes.insurance import router as insurance_router
from app.api.routes.insurance_company import router as insurance_company_router
from app.api.routes.users import router as user_router
from app.api.routes.profiles import router as profiles_router

router = APIRouter()

router.include_router(vehicles_router, prefix='/vehicles', tags=['vehicles'])
router.include_router(insurance_router, prefix='/insurance', tags=['insurance'])
router.include_router(insurance_company_router, prefix='/insurance_company', tags=['insurance_company'])
router.include_router(user_router, prefix='/users', tags=['users'])
router.include_router(profiles_router, prefix='/profiles', tags=['profiles'])
