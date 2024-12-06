from pathlib import Path
from typing import Literal
from db.database import get_db
from db.user_db import get_user_db
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from fastapi.templating import Jinja2Templates
from auth.models import Token, User
from auth.utils import create_access_token, verify_password
from core.config import settings
from auth.dependencies import get_user
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

templates_dir = project_root / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


async def authenticate_user(db, username: str, password: str) -> User | Literal[False]:
    user = await get_user_db(db, username)
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
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
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

