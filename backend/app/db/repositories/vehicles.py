from typing import List
from app.db.repositories.base import BaseRepository
from app.models.vehicles import VehiclesCreate, VehiclesInDB


CREATE_VEHICLES_QUERY = """
    INSERT INTO vehicles (sign, type, model, manufacture_year)
    VALUES (:sign, :type, :model, :manufacture_year)
    ON CONFLICT(sign) DO UPDATE
    SET type=EXCLUDED.type,
        model=EXCLUDED.model,
        manufacture_year=EXCLUDED.manufacture_year  
    RETURNING id, sign, type, model, manufacture_year;

"""

GET_VEHICLE_BY_ID_QUERY = """
    SELECT id, sign, type, model, manufacture_year
    FROM vehicles
    WHERE id = :id;
"""

GET_ALL_VEHICLES_QUERY = """
    SELECT id, sign, type, model, manufacture_year 
    FROM vehicles;  
"""


class VehiclesRepository(BaseRepository):
    """"
    All database actions associated with the Cleaning resource
    """

    async def create_vehicles(self, *, new_vehicle: VehiclesCreate) -> VehiclesInDB:
        query_values = new_vehicle.dict()
        vehicle = await self.db.fetch_one(CREATE_VEHICLES_QUERY, query_values)

        return VehiclesInDB(**vehicle)

    async def get_vehicle_by_id(self, *, id: int) -> VehiclesInDB:
        vehicle = await self.db.fetch_one(query=GET_VEHICLE_BY_ID_QUERY, values={"id": id})
        if not vehicle:
            return None
        return VehiclesInDB(**vehicle)

    async def get_all_vehicles(self) -> List[VehiclesInDB]:
        vehicles_records = await self.db.fetch_all(query=GET_ALL_VEHICLES_QUERY)
        return [VehiclesInDB(**l) for l in vehicles_records]
