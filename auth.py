from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from users import users_list


SECRET_KEY = "segredo-eventos-api"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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
