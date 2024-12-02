from pathlib import Path
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from fastapi.templating import Jinja2Templates
from auth.models import Token, User
from auth.utils import create_access_token, verify_password
from core.config import settings
from db.fake_db import fake_users_db
from auth.dependencies import get_user
from fastapi.responses import RedirectResponse

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

templates_dir = project_root / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


def authenticate_user(fake_db, username: str, password: str) -> User | Literal[False]:
    user = get_user(fake_db, username)
    print("user", user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/token")
async def login_for_access_token(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = RedirectResponse(
        "/", status_code=301,
    )

    response.set_cookie(key="Authorization", value=f"{access_token}", httponly=True)
    return response


@router.get("/login")
async def get_login_form(request: Request):
    return templates.TemplateResponse(
        "login_form.jinja", {"request": request}
    )  

