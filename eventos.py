from fastapi import APIRouter
from pydantic import BaseModel

events_router = APIRouter()

events_list = []


class Event(BaseModel):
    id: int
    nome: str
    organizador_id: int
    token_auditoria: str


@events_router.post("/eventos")
async def add_event(event: Event) -> Event:
    events_list.append(event)
    return event
