from urllib.request import Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import invoices, auth
from app.db.invoices_db import handle_table_creation
import os
from fastapi.responses import RedirectResponse

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(auth.router)
app.include_router(invoices.router)

handle_table_creation()


@app.middleware("http")
async def create_auth_header(
    request: Request,
    call_next,
):
    route = request.url.path
    if "Authorization" not in request.headers and "Authorization" in request.cookies:
        access_token = request.cookies["Authorization"]

        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer {access_token}".encode(),
            )
        )
    if (
        "Authorization" not in request.headers
        and route != "/login"
        and route != "/token"
    ):
        return RedirectResponse(url="/login")

    response = await call_next(request)
    return response
