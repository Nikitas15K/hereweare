import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from app.models.insurance import InsuranceAdd, InsuranceInDB

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_insurance():
    return InsuranceAdd(
        number="JA651914",
        expire_date=1640993759,
        vehicle_id=1,
        insurance_company_id=1,
    )


class TestInsuranceRoutes:

    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("insurance: add-insurance"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("insurance: add-insurance"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestAddInsurance:
    # async def test_valid_input_adds_insurance(
    #     self, app: FastAPI, client: AsyncClient, new_insurance: InsuranceAdd
    # ) -> None:
    #
    #     res = await client.post(
    #         app.url_path_for("insurance: add-insurance"), json={"new_insurance": new_insurance.dict()}
    #     )
    #     assert res.status_code == HTTP_201_CREATED
    #
    #     added_insurance = InsuranceAdd(**res.json())
    #     assert added_insurance == new_insurance

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
                (None, 422),
                ({}, 422),
                ({"number": "test_name"}, 422),
                ({"expire_date": 1640993759}, 422),
                ({"number": "test_name", "expire_date": 1640993759}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
            self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("insurance: add-insurance"), json={"new_insurance": invalid_payload}
        )
        assert res.status_code == status_code
