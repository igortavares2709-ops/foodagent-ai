from collections.abc import Callable
from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI, HTTPException, Path, Request

from agente import atender
from ferramentas import simular_cancelamento
from observabilidade import incrementar, metricas, middleware_observabilidade
from repositorio_postgres import buscar_pedido_postgres
from schemas import (
    CancelamentoRequest,
    CancelamentoResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    MetricasResponse,
    PedidoResponse,
)

app = FastAPI(
    title="FoodAgent AI",
    description="Agente de atendimento de delivery com dados e ações fictícios.",
    version="1.0.0",
)
app.middleware("http")(middleware_observabilidade)

BuscadorPedidos = Callable[[str], PedidoResponse | None]


def obter_buscador() -> BuscadorPedidos:
    return buscar_pedido_postgres


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", application="FoodAgent AI")


@app.get("/metrics", response_model=MetricasResponse)
def obter_metricas() -> MetricasResponse:
    return MetricasResponse(**metricas())


@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(
    pedido_id: Annotated[
        str,
        Path(pattern=r"^PED-[0-9]{3}$", description="Exemplo: PED-001"),
    ],
    buscador: Annotated[BuscadorPedidos, Depends(obter_buscador)],
) -> PedidoResponse:
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


@app.post("/chat", response_model=ChatResponse)
def chat(entrada: ChatRequest, request: Request) -> ChatResponse:
    incrementar("chats")
    try:
        estado = atender(entrada.mensagem, entrada.pedido_id)
    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Atendimento temporariamente indisponível.",
        ) from None
    return ChatResponse(
        resposta=estado["resposta"],
        intencao=estado["intencao"],
        fontes=estado.get("fontes", []),
        requer_humano=estado.get("requer_humano", False),
        request_id=request.state.request_id,
    )


@app.post("/acoes/cancelamento", response_model=CancelamentoResponse)
def cancelar(entrada: CancelamentoRequest) -> CancelamentoResponse:
    acao = simular_cancelamento(entrada.pedido_id, entrada.motivo)
    return CancelamentoResponse(**acao.__dict__)
