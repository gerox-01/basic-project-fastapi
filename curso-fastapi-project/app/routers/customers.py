from sqlite3 import IntegrityError
from typing import List

from db import SessionDep
from fastapi import APIRouter, HTTPException, Query, status
from models import (CustomerCreateModel, CustomerModel, CustomerPlanLink,
                    CustomerUpdateModel, PlanModel, StatusEnum)
from sqlmodel import select

router = APIRouter(tags = ['Customers'])

@router.post("/customers", response_model=CustomerModel, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreateModel, session: SessionDep):
    try:
        customer = CustomerModel.model_validate(customer.model_dump())
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail="A customer with this email already exists."
        )
    
@router.get("/customers", response_model=List[CustomerModel], status_code=status.HTTP_200_OK)
async def get_customers(session: SessionDep):
    try:
        return session.exec(select(CustomerModel)).all()
    except Exception as e:
        return {"error": str(e)}

@router.get("/customers/{customer_id}", response_model=CustomerModel, status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, session: SessionDep):
    try:
        customer = session.exec(select(CustomerModel).where(CustomerModel.id == customer_id)).first()
        if customer:
            return customer
        else:
            return{'messsage':'Cliente no encontrado'}
    except IndexError:
        raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/customers/{customer_id}", response_model=CustomerModel, status_code=status.HTTP_200_OK)
async def update_customer(customer_id: int, customer: CustomerUpdateModel, session: SessionDep):
    try:
        customer_db = session.exec(CustomerModel).get(customer_id)
        if customer_db == None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        old_data = customer_db
        update_data = customer.model_dump(exclude_unset=True)
        # Check if the data is different from the old data
        if old_data.name != update_data['name']:
            update_data['name'] = old_data.name
        if old_data.description != update_data['description']:
            update_data['description'] = old_data.description
        if old_data.email != update_data['email']:
            update_data['email'] = old_data.email    
        if old_data.age != update_data['age']:
            update_data['age'] = old_data.age

        customer.sqlmodel_update(update_data)
        session.add(customer)
        session.commit()
        session.refresh(customer)
    except Exception as e:
        return {"error": str(e)}
    
@router.delete("/customers/{customer_id}", status_code=status.HTTP_200_OK)
async def delete_customer(customer_id: int, session: SessionDep):
    try:
        customer_db = session.exec(CustomerModel).get(customer_id)
        if customer_db == None:
            return {"message": "Customer not found"}
        session.delete(customer_db)
        session.commit()
        return {"message": f"Customer '{customer_id}' deleted"}
    except Exception as e:
        return {"error": str(e)}

@router.post("/customers/{customer_id}/subscribe/{plan_id}", status_code=status.HTTP_200_OK)
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    try:
        customer_db = session.exec(select(CustomerModel).where(CustomerModel.id == customer_id)).first()
        if customer_db is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        plan_db = session.exec(select(PlanModel).where(PlanModel.id == plan_id)).first()
        if plan_db is None:
            raise HTTPException(status_code=404, detail="Plan not found")

        existing_link = session.exec(
            select(CustomerPlanLink).where(
                CustomerPlanLink.customer_id == customer_id,
                CustomerPlanLink.plan_id == plan_id
            )
        ).first()

        if existing_link:
            raise HTTPException(status_code=400, detail="Customer is already subscribed to this plan")

        customer_plan_db = CustomerPlanLink(customer_id=customer_id, plan_id=plan_id, status=plan_status)
        session.add(customer_plan_db)
        session.commit()
        session.refresh(customer_plan_db)

        return {"message": f"Customer '{customer_id}' subscribed to plan '{plan_id}' with status '{plan_status}'"}
    except Exception as e:
        return {"error": str(e)}

    

@router.get("/customers/{customer_id}/plans", status_code=status.HTTP_200_OK)
async def obtain_subscribe_customer_to_plans(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    try:
        customer_db = session.exec(select(CustomerModel).where(CustomerModel.id == customer_id)).first()
        if customer_db == None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        plans = session.exec(select(CustomerPlanLink).where(CustomerPlanLink.customer_id == customer_id, CustomerPlanLink.status == plan_status)).all()
        return plans
    except Exception as e:
        return {"error": str(e)}
    