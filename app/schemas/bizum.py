from pydantic import BaseModel

#Representa un evento de Bizum listo para salir por API.
class BizumEventPublic(BaseModel):
    bizum_id: str
    booking_date: str
    amount: float
    currency: str
    direction: str
    counterparty: str
    concept: str
    status: str

#Agrupa la lista de Bizum con un count
class BizumListResponse(BaseModel):
    items: list[BizumEventPublic]
    count: int