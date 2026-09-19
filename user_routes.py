from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm

from users import User, users_list, hash_password, verify_password
from auth import create_access_token


users_router = APIRouter()


@users_router.post("/signup")
async def signup(user: User) -> dict:
    for existing_user in users_list:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=400,
                detail="Usuário já cadastrado."
            )

    user.password = hash_password(user.password)
    users_list.append(user)

    return {
        "message": "Usuário cadastrado com sucesso."
    }


@users_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    mfa_code: str = Form(None)
) -> dict:
    for user in users_list:
        if user.username == form_data.username:

            if verify_password(form_data.password, user.password):

                if user.role == "administrador":
                    if mfa_code != "123456":
                        raise HTTPException(
                            status_code=401,
                            detail="Código MFA inválido."
                        )

                token = create_access_token(user)

                return {
                    "access_token": token,
                    "token_type": "bearer"
                }

    raise HTTPException(
        status_code=401,
        detail="Usuário ou senha inválidos."
    )
