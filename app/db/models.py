from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from datetime import datetime

class User(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    password_hash: str

    accounts: List["Account"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: str = Field(index=True, unique=True)
    user_id: str = Field(foreign_key="user.user_id", index=True)
    iban: str
    alias: str
    balance: float
    currency: str = "EUR"

    user: Optional[User] = Relationship(back_populates="accounts")

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(index=True, unique=True)
    user_id: str = Field(foreign_key="user.user_id", index=True)
    account_id: str = Field(foreign_key="account.account_id", index=True)
    booking_date: date
    amount: float
    currency: str = "EUR"
    description: str
    category: str

class BizumEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bizum_id: str = Field(index=True, unique=True)
    user_id: str = Field(foreign_key="user.user_id", index=True)
    booking_date: date
    amount: float
    currency: str = "EUR"
    direction: str
    counterparty: str
    concept: str
    status: str = "completed"

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True)
    user_id: str = Field(index=True)
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)