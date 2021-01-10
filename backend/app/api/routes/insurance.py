from typing import List
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED
from app.models.insurance import InsuranceAdd, InsurancePublic
from app.db.repositories.insurance import InsuranceRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/", response_model=List[InsurancePublic], name="vehicles:get-all-vehicles")
async def get_all_insurances(
        insurances_repo: InsuranceRepository = Depends(get_repository(InsuranceRepository))
) -> List[InsurancePublic]:
    return await insurances_repo.get_all_insurances()


@router.post("/", response_model=InsurancePublic, name="insurance: add-insurance", status_code=HTTP_201_CREATED)
async def add_new_insurance(
    new_insurance: InsuranceAdd = Body(..., embed=True),
    insurance_repo: InsuranceRepository = Depends(get_repository(InsuranceRepository)),
) -> InsurancePublic:
    added_insurance = await insurance_repo.add_insurance(new_insurance=new_insurance)
    return added_insurance
