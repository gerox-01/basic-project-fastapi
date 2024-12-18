from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

sqlite_name = "db.sqlite3"
sqlite_url = f'sqlite:///{sqlite_name}'


engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}
)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]