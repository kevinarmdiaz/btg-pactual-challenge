from datetime import datetime
from typing import TypeVar

from typing import List, Optional
from uuid import UUID, uuid4

from beanie import Document, PydanticObjectId, Link, Insert, Replace
from pydantic import Field, UUID4

# ### 🧑🏽‍💼Colección: user
# _id: ObjectId
# name: String
# email: String
# phone: String
# balance: Int64
#
# ### 📈 Colección: funds
# _id: ObjectId
# name: String
# category: String
# minimum_investment_amount: Int32
#
# ###  📝📈 Colección: log_transactions_funds
# *_id: ObjectId
# --
# user_id: ObjectId
# fund_id: Int32
# transaction_type: String -> Might
# be[Apertura, Cancelación]
# message: String
# balance: Int64
# date: IsoDate

__all__ = (
    "Document", "UsersCollection", "FundsCollection",
    "LogTransactionsFundsCollection", "ConcreteCollection", "SubscriptionCollection"
)

from src.infrastructure.application.errors.entities import InsufficientBalanceError


class _Document(Document):
    """Base class for all database collections."""
    id: UUID = Field(default_factory=uuid4)


ConcreteCollection = TypeVar("ConcreteCollection", bound=_Document)


class FundsCollection(_Document):
    name: str
    category: str
    minimum_investment_amount: int

    class Settings:
        name = "funds"  # Collection name in MongoDB


class UsersCollection(_Document):
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's email")
    phone: str = Field(..., description="User's phone number")
    balance: int = Field(..., description="User's balance in Int64 format")

    class Settings:
        use_state_management = True
        name = "users"  # Collection name in MongoDB
    
    async def check_balance(self, fund_instance: FundsCollection):
        """

        :param fund_instance:
        """
        if self.balance < fund_instance.minimum_investment_amount:
            raise InsufficientBalanceError(
                balance=self.balance,
                fund_name=fund_instance.name,
                minimum_investment=fund_instance.minimum_investment_amount,
                instance=f"/subscription/subscribe-fund"
            )
    
    async def add_balance(self, minimum_investment_amount: int):
        """

        :param minimum_investment_amount:
        :param user:
        :param fund:
        """
        self.balance += minimum_investment_amount

    async def reduce_balance(self, minimum_investment_amount: int):
        """

        :param minimum_investment_amount:
        :param user:
        :param fund:
        """
        self.balance -= minimum_investment_amount


# 📝📈 Log Transactions Funds Collection
class LogTransactionsFundsCollection(_Document):
    user_id: UUID4 = Field(..., description="Reference to the user ID")
    fund_id: UUID4 = Field(..., description="Reference to the fund ID")
    transaction_type: str = Field(..., description="Type of transaction (Apertura, Cancelación)")
    message: Optional[str] = Field(None, description="Additional message or details")
    balance: int = Field(..., description="User's balance after the transaction in Int64 format")
    date: datetime = Field(default_factory=datetime.now, description="Date of the transaction")

    class Settings:
        name = "log_transactions_funds"  # Collection name in MongoDB

# 📝📈 Manage subscriptions
class SubscriptionCollection(_Document):
    user: Link[UsersCollection]
    fund: Link[FundsCollection]
    subscription_date: Optional[datetime] = Field(default_factory=datetime.now, description="Date of the transaction")

    class Settings:
        name = "subscriptions"
    
    # @after_event([Insert, Replace])
    # async def send_callback(self):
    #     pass