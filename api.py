from collections.abc import Callable
from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Path

from repositorio_postgres import buscar_pedido_postgres
from schemas import HealthResponse, PedidoResponse


app = FastAPI(
    title="FoodAgent AI",
    description="API de atendimento de delivery com dados fictícios.",
    version="0.1.0",
)

BuscadorPedidos = Callable[[str], PedidoResponse | None]


def obter_buscador() -> BuscadorPedidos:
    """Define o repositório usado pela API."""
    return buscar_pedido_postgres


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
    buscador: Annotated[BuscadorPedidos, Depends(obter_buscador)],
) -> PedidoResponse:
    """Consulta um pedido persistido no PostgreSQL."""
    try:
        pedido = buscador(pedido_id)
    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Consulta de pedidos temporariamente indisponível.",
        ) from None
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="Falha interna ao consultar o pedido.",
        ) from None

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return pedido