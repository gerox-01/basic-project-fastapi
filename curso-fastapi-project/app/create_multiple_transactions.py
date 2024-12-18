import sys
from pathlib import Path

# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db import engine
from models import CustomerModel, TransactionModel
from sqlmodel import Session, select


def create_multiple_transactions():
    """
    Creates initial fake transactions for testing purposes.
    """
    try:
        with Session(engine) as session:
            # Verificar si ya existen datos
            existing_customer = session.exec(select(CustomerModel)).first()
            if existing_customer:
                print("Fake data already exists. Skipping...")
                return

            # Crear un cliente de prueba
            customer = CustomerModel(
                name="Luis",
                description="Profe Platzi",
                email="hola@lcmartinez.com",
                age=33,
            )
            session.add(customer)
            session.commit()

            # Crear 100 transacciones
            for x in range(100):
                transaction = TransactionModel(
                    customer_id=customer.id,
                    description=f"Test number {x}",
                    amount=10 * x,
                )
                session.add(transaction)
            session.commit()
            print("Fake data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise e


if __name__ == "__main__":
    create_multiple_transactions()
