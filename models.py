from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nome: str
    data: str
    organizador_id: int
    token_auditoria: str


class EventResponse(SQLModel):
    id: int
    nome: str

    model_config = {
        "extra": "forbid"
    }


class Inscricao(SQLModel, table=True):
    id: int = Field(primary_key=True)
    usuario_id: int
    evento: str


class Comentario(SQLModel, table=True):
    id: int = Field(primary_key=True)
    evento_id: int
    comentario: str
