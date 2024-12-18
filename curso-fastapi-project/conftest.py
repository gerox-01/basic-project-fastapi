import pytest
from app.main import app
from db import Session, SQLModel, get_session
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine

sqlite_name_test = "db_test.sqlite3"
sqlite_url = f'sqlite:///{sqlite_name_test}'

engine_test = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool,
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        yield session
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_overrides():
        return session

    app.dependency_overrides[get_session] = get_session_overrides
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()