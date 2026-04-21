from datetime import date
from pydantic import BaseModel


# Representa un movimiento bancario en formato público para API.
class TransactionPublic(BaseModel):
    transaction_id: str
    account_id: str
    booking_date: date
    amount: float
    currency: str
    description: str
    category: str


# Agrupa la lista de movimientos junto con un contador count.
class TransactionListResponse(BaseModel):
    items: list[TransactionPublic]
    count: int
