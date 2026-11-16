from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel


app = FastAPI(
    title="FoodAgent AI",
    description="API de atendimento de delivery com dados fictícios.",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    application: str


class PedidoResponse(BaseModel):
    id: str
    status: Literal["em preparo", "em entrega", "entregue"]


PEDIDOS_FICTICIOS = {
    "PED-001": PedidoResponse(id="PED-001", status="em preparo"),
    "PED-002": PedidoResponse(id="PED-002", status="entregue"),
}


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Confirma que a aplicação está respondendo."""
    return HealthResponse(status="ok", application="FoodAgent AI")


@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(
    pedido_id: Annotated[
        str,
        Path(pattern=r"^PED-[0-9]{3}$", description="Exemplo: PED-001"),
    ],
) -> PedidoResponse:
    """Consulta um pedido fictício armazenado em memória."""
    pedido = PEDIDOS_FICTICIOS.get(pedido_id)

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return pedido