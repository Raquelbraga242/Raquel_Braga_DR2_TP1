from pydantic import BaseModel
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    id: int
    username: str
    password: str
    role: str = "organizador"


users_list = []


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
