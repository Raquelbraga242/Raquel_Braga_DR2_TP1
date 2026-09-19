
from pydantic import BaseModel


class Event(BaseModel):
    id: int
    nome: str
    data: str
    organizador_id: int
    token_auditoria: str


class EventResponse(BaseModel):
    id: int
    nome: str
