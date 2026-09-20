import re
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

from models import Event, EventResponse
from database import events_list, inscricoes_list, comentarios_list
from auth import get_current_user, check_inscricao_ownership


events_router = APIRouter()

templates = Jinja2Templates(directory="templates")


event_requests = {}


def check_event_rate_limit(ip: str):
    now = datetime.now(timezone.utc)

    if ip not in event_requests:
        event_requests[ip] = []

    event_requests[ip] = [
        request_time
        for request_time in event_requests[ip]
        if now - request_time < timedelta(minutes=1)
    ]

    if len(event_requests[ip]) >= 30:
        raise HTTPException(
            status_code=429,
            detail="Muitas requisições. Tente novamente mais tarde."
        )

    event_requests[ip].append(now)


@events_router.post("/eventos", response_model=EventResponse)
async def add_event(
    event: Event,
    current_user=Depends(get_current_user)
) -> Event:
    events_list.append(event)
    return event


@events_router.get("/eventos")
async def retrieve_events(request: Request) -> dict:
    ip = request.client.host
    check_event_rate_limit(ip)

    return {
        "events": events_list
    }


@events_router.get("/eventos/busca")
async def search_events(nome: str) -> dict:
    if not re.fullmatch(r"[a-zA-ZÀ-ÿ0-9 ]+", nome):
        raise HTTPException(
            status_code=400,
            detail="Termo de busca inválido."
        )

    query = "SELECT * FROM eventos WHERE nome = '" + nome + "'"

    return {
        "query": query
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


@events_router.get("/inscricoes/{inscricao_id}")
async def get_inscricao(
    inscricao_id: int,
    current_user=Depends(get_current_user)
):
    for inscricao in inscricoes_list:
        if inscricao["id"] == inscricao_id:
            check_inscricao_ownership(inscricao, current_user)

            return {
                "inscricao": inscricao
            }

    raise HTTPException(
        status_code=404,
        detail="Inscrição não encontrada."
    )


@events_router.post("/eventos/{evento_id}/comentarios")
async def add_comentario(evento_id: int, comentario: str):
    comentarios_list.append({
        "evento_id": evento_id,
        "comentario": comentario
    })

    return {
        "message": "Comentário cadastrado com sucesso."
    }


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
                context={
                    "evento": evento,
                    "comentarios": comentarios_list
                }
            )

    return {
        "message": "Evento não encontrado."
    }
