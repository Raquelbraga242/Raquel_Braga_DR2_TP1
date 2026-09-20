from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from users import users_list


SECRET_KEY = "segredo-eventos-api"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


login_attempts = {}


def check_login_rate_limit(ip: str):
    now = datetime.now(timezone.utc)

    if ip not in login_attempts:
        login_attempts[ip] = []

    login_attempts[ip] = [
        attempt
        for attempt in login_attempts[ip]
        if now - attempt < timedelta(minutes=1)
    ]

    if len(login_attempts[ip]) >= 5:
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas de login. Tente novamente mais tarde."
        )

    login_attempts[ip].append(now)


def create_access_token(user):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data = {
        "sub": str(user.id),
        "role": user.role,
        "exp": expire
    }

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido."
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado."
        )

    for user in users_list:
        if str(user.id) == user_id:
            return user

    raise HTTPException(
        status_code=401,
        detail="Usuário não encontrado."
    )


def check_inscricao_ownership(inscricao, current_user):
    if inscricao["usuario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem acesso a esta inscrição."
        )

    return inscricao
