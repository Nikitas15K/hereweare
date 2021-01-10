from typing import List
from app.db.repositories.base import BaseRepository
from app.models.insurance import InsuranceAdd, InsuranceInDB

ADD_INSURANCE_QUERY = """
    INSERT INTO insurance (number, expire_date, vehicle_id, insurance_company_id)
    VALUES (:number, :expire_date, :vehicle_id, :insurance_company_id)
    RETURNING id, number, expire_date, vehicle_id, insurance_company_id;
"""

GET_ALL_INSURANCES_QUERY = """
    SELECT id, number, expire_date, vehicle_id, insurance_id 
    FROM insurance;  
"""


class InsuranceRepository(BaseRepository):
    """"
    All database actions associated with the Cleaning resource
    """
    async def add_insurance(self, *, new_insurance: InsuranceAdd) -> InsuranceInDB:
        query_values = new_insurance.dict()
        insurance = await self.db.fetch_one(query=ADD_INSURANCE_QUERY, values=query_values)
        return InsuranceInDB(**insurance)

    async def get_all_insurances(self) -> List[InsuranceInDB]:
        insurances_records = await self.db.fetch_all(query=GET_ALL_INSURANCES_QUERY)
        return [InsuranceInDB(**l) for l in insurances_records]
