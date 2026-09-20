from sqlmodel import SQLModel, Session, create_engine

from settings import settings
from models import Event, Inscricao, Comentario

engine = create_engine(
    settings.database_url,
    echo=True
)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
