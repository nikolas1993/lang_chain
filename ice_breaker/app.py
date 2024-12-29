from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import app_router

load_dotenv()

app = FastAPI()
app.include_router(app_router.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

