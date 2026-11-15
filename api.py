from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="FoodAgent AI",
    description="API de atendimento de delivery com dados fictícios.",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    application: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Confirma que a aplicação está respondendo."""
    return HealthResponse(
        status="ok",
        application="FoodAgent AI",
    )