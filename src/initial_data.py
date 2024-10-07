import logging

from src.infrastructure.mongodb import FundsCollection, UsersCollection
from src.infrastructure.mongodb.services.transactions import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from typing import List

async def init() -> None:
    """
    Init database with funds if they do not already exist
    """

    await init_db()
    # List of funds to insert
    funds_data = [
        {
            "name": "FPV_BTG_PACTUAL_RECAUDADORA",
            "category": "FPV",
            "minimum_investment_amount": 75000
        },
        {
            "name": "FPV_BTG_PACTUAL_ECOPETROL",
            "category": "FPV",
            "minimum_investment_amount": 125000
        },
        {
            "name": "DEUDAPRIVADA",
            "category": "FIC",
            "minimum_investment_amount": 50000
        },
        {
            "name": "FDO-ACCIONES",
            "category": "FIC",
            "minimum_investment_amount": 250000
        },
        {
            "name": "FPV_BTG_PACTUAL_DINAMICA",
            "category": "FPV",
            "minimum_investment_amount": 100000
        }
    ]

    users_data = [
        {
            "name": "Kevin Diaz",
            "email": "kevindiaz9511@gmail.com",
            "phone": "3012368027",
            "balance": 500000
        },
    ]

    for user in users_data:
        existing_user = await UsersCollection.find_one({"name": user["name"]})
        if not existing_user:
            new_user = UsersCollection(
                name=user["name"],
                email=user["email"],
                phone=user["phone"],
                balance=user["balance"]
            )
            await new_user.insert()
            print(f"Inserted User: {user['name']}")

    for fund in funds_data:
        existing_fund = await FundsCollection.find_one({"name": fund["name"]})

        if not existing_fund:
            new_fund = FundsCollection(
                name=fund["name"],
                category=fund["category"],
                minimum_investment_amount=fund["minimum_investment_amount"]
            )
            await new_fund.insert()
            print(f"Inserted fund: {fund['name']}")
        else:
            print(f"Fund already exists: {fund['name']}")




    print("..: Finishing db initialization :::..")


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
