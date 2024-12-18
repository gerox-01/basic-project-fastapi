from datetime import datetime
from enum import Enum
from typing import List, Optional

from db import engine
from pydantic import EmailStr, field_validator
from sqlmodel import Field, Relationship, Session, SQLModel, select


class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

class CustomerPlanLink(SQLModel, table=True):
    customer_id: Optional[int] = Field(default=None, foreign_key="customermodel.id", primary_key=True)
    plan_id: Optional[int] = Field(default=None, foreign_key="planmodel.id", primary_key=True)
    status: StatusEnum = Field(default=StatusEnum.active)
    
class PlanBaseModel(SQLModel):
    name: str | None = Field(default=None, unique=True)
    description: Optional[str] = None
    price: float

class PlanCreateModel(PlanBaseModel):
    pass

class PlanModel(PlanBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    customers: List["CustomerModel"] = Relationship(back_populates="plans", link_model=CustomerPlanLink)
    active: bool = Field(default=True)

class CustomerBaseModel(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(CustomerModel).where(CustomerModel.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("Email already exists")
        return value

class CustomerModel(CustomerBaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: List["TransactionModel"] = Relationship(back_populates="customer")
    plans: List["PlanModel"] = Relationship(back_populates="customers", link_model=CustomerPlanLink)

class CustomerCreateModel(CustomerBaseModel):
    pass

class CustomerUpdateModel(CustomerBaseModel):
    pass

class TransactionBaseModel(SQLModel):
    amount: Optional[float] = Field(default=None)
    description: Optional[str] = Field(default=None)

class TransactionModel(TransactionBaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    customer: List["CustomerModel"] = Relationship(back_populates="transactions")
    customer_id: int = Field(foreign_key="customermodel.id")

class TransactionCreateModel(TransactionBaseModel):
    customer_id: int
    
class PaginatedTransactionsResponse(SQLModel):
    total_count: int
    total_pages: int 
    current_page: int
    limit: int
    transactions: List["TransactionModel"] 