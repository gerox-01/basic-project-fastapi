from db import SessionDep
from fastapi import APIRouter, status
from models import PlanCreateModel, PlanModel
from sqlmodel import select

router = APIRouter(tags=["Plans"])

@router.post("/plans", status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data: PlanCreateModel, session: SessionDep):
    try:
        plan_data_dict = plan_data.model_dump()
        plan_db = PlanModel(**plan_data_dict)
        session.add(plan_db)
        session.commit()
        session.refresh(plan_db)

        return plan_db
    except Exception as e:
        return {"error": str(e)}

    

@router.get("/plans", status_code=status.HTTP_200_OK, response_model=list[PlanModel])
async def get_plans(session: SessionDep):
    try:
        plans = session.exec(select(PlanModel)).all()
        return plans
    except Exception as e:
        return {"error": str(e)}
    