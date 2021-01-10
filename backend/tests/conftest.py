import warnings
import uuid
import os
import pytest
import docker as pydocker
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config
from app.models.vehicles import VehiclesCreate, VehiclesInDB
from app.db.repositories.vehicles import VehiclesRepository
from app.models.insurance import InsuranceAdd, InsuranceInDB
from app.db.repositories.insurance import InsuranceRepository
from app.models.insurance_company import InsuranceCompanyCreate, InsuranceCompanyInDB
from app.db.repositories.insurance_company import InsuranceCompanyRepository
from app.models.user import UserCreate, UserInDB
from app.db.repositories.users import UsersRepository

from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from app.services import auth_service


@pytest.fixture(scope="session")
def docker() -> pydocker.APIClient:
    # base url is the unix socket we use to communicate with docker
    return pydocker.APIClient(base_url="unix://var/run/docker.sock", version="auto")


@pytest.fixture(scope="session", autouse=True)
def postgres_container(docker: pydocker.APIClient) -> None:
    """
    Use docker to spin up a postgres container for the duration of the testing session.

    Kill it as soon as all tests are run.

    DB actions persist across the entirety of the testing session.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # pull image from docker
    image = "postgres:12.1-alpine"
    docker.pull(image)

    # create the new container using
    # the same image used by our database
    container = docker.create_container(
        image=image,
        name=f"test-postgres-{uuid.uuid4()}",
        detach=True,
    )

    docker.start(container=container["Id"])

    config = alembic.config.Config("alembic.ini")

    try:
        os.environ["DB_SUFFIX"] = "_test"
        alembic.command.upgrade(config, "head")
        yield container
        alembic.command.downgrade(config, "base")
    finally:
        # remove container
        docker.kill(container["Id"])
        docker.remove_container(container["Id"])


# Create a new application for testing
@pytest.fixture
def app() -> FastAPI:
    from app.api.server import get_application

    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
                app=app,
                base_url="http://testserver",
                headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest.fixture
async def test_vehicle(db: Database) -> VehiclesInDB:
    vehicle_repo = VehiclesRepository(db)
    new_vehicle = VehiclesCreate(
        sign="JAK 1914",
        type="car",
        model="Porches",
        manufacture_year=2019,
    )
    return await vehicle_repo.create_vehicles(new_vehicle=new_vehicle)


@pytest.fixture
async def test_insurance(db: Database) -> InsuranceInDB:
    insurance_repo = InsuranceRepository(db)
    new_insurance = InsuranceAdd(
        number="JA651914",
        expire_date=1640993759,
        vehicle_id=1,
        insurance_company_id=1,
    )
    return await insurance_repo.add_insurance(new_insurance=new_insurance)


@pytest.fixture
async def test_insurance_company(db: Database) -> InsuranceCompanyInDB:
    insurance_company_repo = InsuranceCompanyRepository(db)
    new_insurance_company = InsuranceCompanyCreate(
        name="herewego",
        email="hereyoutest@herewego.gr",
    )
    existing_insurance_company = await insurance_company_repo.get_insurance_company_by_email(email=new_insurance_company.email)
    if existing_insurance_company:
        return existing_insurance_company
    return await insurance_company_repo.create_insurance_company(new_insurance_company=new_insurance_company)


@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="lebron@james.io",
        username="lebronjames",
        password="heatcavslakers",
    )
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


@pytest.fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client


@pytest.fixture
async def test_user2(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="serena@williams.io",
        username="serenawilliams",
        password="tennistwins",
    )
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user

    return await user_repo.register_new_user(new_user=new_user)

