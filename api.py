from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from schemas import HealthResponse, PedidoResponse


app = FastAPI(
    title="FoodAgent AI",
    description="API de atendimento de delivery com dados fictícios.",
    version="0.1.0",
)



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
    pedido = pedido = buscar_pedido(pedido_id)

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return pedido
from repositorio_pedidos import buscar_pedido