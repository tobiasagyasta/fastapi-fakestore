from fastapi import FastAPI

from app.infrastructure.db.engine import init_db
from app.presentation.api.products_router import router as products_router

app = FastAPI()

app.include_router(products_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "Welcome to Toby's Fake Store API"}
