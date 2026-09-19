from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from models import Event, EventResponse
from database import events_list
from auth import get_current_user


events_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@events_router.post("/eventos", response_model=EventResponse)
async def add_event(
    event: Event,
    current_user=Depends(get_current_user)
) -> Event:
    events_list.append(event)
    return event


@events_router.get("/eventos")
async def retrieve_events() -> dict:
    return {
        "events": events_list
    }


@events_router.get("/eventos/{evento_id}")
async def get_single_event(evento_id: int) -> dict:
    for evento in events_list:
        if evento.id == evento_id:
            return {
                "evento": evento
            }

    return {
        "message": "Evento não encontrado."
    }


@events_router.put("/eventos/{evento_id}")
async def edit_event(
    evento_id: int,
    event: Event,
    current_user=Depends(get_current_user)
) -> Event:
    for evento in events_list:
        if evento.id == evento_id:

            if evento.organizador_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Você não é o organizador deste evento."
                )

            evento.nome = event.nome
            evento.data = event.data

            return evento

    raise HTTPException(
        status_code=404,
        detail="Evento não encontrado."
    )


@events_router.get("/eventos-html")
async def eventos_html(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="eventos.html",
        context={"eventos": events_list}
    )


@events_router.get("/eventos-html/{evento_id}")
async def evento_html(request: Request, evento_id: int):
    for evento in events_list:
        if evento.id == evento_id:
            return templates.TemplateResponse(
                request=request,
                name="evento.html",
                context={"evento": evento}
            )

    return {
        "message": "Evento não encontrado."
    }
