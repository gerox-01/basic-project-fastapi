
from fastapi import APIRouter

router = APIRouter(tags=["Invoices"])

@router.get("/invoices")
async def get_list_invoice():
    return {"message": "get_list invoice"}
