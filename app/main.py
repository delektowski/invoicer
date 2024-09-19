from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import invoices
from app.db.invoices_db import handle_table_creation
import os

app = FastAPI()

# Get the directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the static directory
static_dir = os.path.join(current_dir, "static")

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(invoices.router)

handle_table_creation()

