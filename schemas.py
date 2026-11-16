from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    application: str


class PedidoResponse(BaseModel):
    id: str
    status: Literal["em preparo", "em entrega", "entregue"]
