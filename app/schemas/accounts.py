from pydantic import BaseModel


class AccountPublic(BaseModel):
    account_id: str
    iban: str
    alias: str
    balance: float
    currency: str


class BalanceSummary(BaseModel):
    user_id: str
    currency: str
    total_balance: float
    account_count: int


class AccountBalanceItem(BaseModel):
    account_id: str
    alias: str
    balance: float
    currency: str


class BalanceSummaryDetailed(BaseModel):
    user_id: str
    currency: str
    total_balance: float
    account_count: int
    accounts: list[AccountBalanceItem]
