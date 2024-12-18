from db import SessionDep
from fastapi import APIRouter, HTTPException, Query, status
from models import (CustomerModel, PaginatedTransactionsResponse,
                    TransactionCreateModel, TransactionModel)
from sqlmodel import select

router = APIRouter(tags=["Transactions"])

@router.get("/transactions", status_code=status.HTTP_200_OK, response_model=PaginatedTransactionsResponse)
async def get_transactions(session: SessionDep, skip: int = Query(0, description="Number of transactions to skip"), limit: int = Query(10, description="Number of transactions to retrieve")):
    try:
        # Consulta de transacciones con paginación
        query = select(TransactionModel).offset(skip).limit(limit)
        transactions = session.exec(query).all()

        # Obtener el total de registros en la base de datos (sin paginación)
        total_count_query = select(TransactionModel)
        total_count = len(session.exec(total_count_query).all())  # Contamos los registros

        # Calcular el total de páginas
        total_pages = (total_count + limit - 1) // limit  # Redondear hacia arriba

        # Crear la respuesta paginada
        response = PaginatedTransactionsResponse(
            total_count=total_count,
            total_pages=total_pages,
            current_page=(skip // limit) + 1,  # Calcular la página actual
            limit=limit,
            transactions=transactions
        )

        return response
    except Exception as e:
        return {"error": str(e)}

    
@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreateModel, session: SessionDep):
    try:
        transaction_data_dict = transaction_data.model_dump()
        customer = session.get(CustomerModel, transaction_data_dict.get("customer_id"))
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        
        transaction_db = TransactionModel.model_validate(transaction_data_dict)
        session.add(transaction_db)
        # Commit the transaction
        session.commit()
        # Refresh the object to get the customer relationship
        session.refresh(transaction_db)
        return transaction_db
    except Exception as e:
        return {"error": str(e)}

