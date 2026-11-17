from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"]
    application: str


class PedidoResponse(BaseModel):
    id: str
    status: Literal["em preparo", "em entrega", "entregue"]


class ChatRequest(BaseModel):
    mensagem: str = Field(min_length=1, max_length=1000)
    pedido_id: str | None = Field(default=None, pattern=r"^PED-[0-9]{3}$")


class ChatResponse(BaseModel):
    resposta: str
    intencao: str
    fontes: list[str]
    requer_humano: bool
    request_id: str


class CancelamentoRequest(BaseModel):
    pedido_id: str = Field(pattern=r"^PED-[0-9]{3}$")
    motivo: str = Field(min_length=3, max_length=300)


class CancelamentoResponse(BaseModel):
    protocolo: str
    acao: Literal["cancelamento"]
    pedido_id: str
    executada: Literal[False]
    mensagem: str
    criado_em: str


class MetricasResponse(BaseModel):
    requisicoes: int
    erros: int
    chats: int
