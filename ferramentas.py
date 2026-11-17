"""Ferramentas deterministicas e acoes simuladas do FoodAgent."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from repositorio_postgres import buscar_pedido_postgres


@dataclass(frozen=True)
class AcaoSimulada:
    protocolo: str
    acao: str
    pedido_id: str
    executada: bool
    mensagem: str
    criado_em: str


def consultar_status(pedido_id: str):
    return buscar_pedido_postgres(pedido_id)


def simular_cancelamento(pedido_id: str, motivo: str) -> AcaoSimulada:
    """Registra apenas a intencao; nunca altera o pedido real ou ficticio."""
    motivo = motivo.strip()
    if not motivo:
        raise ValueError("O motivo do cancelamento e obrigatorio.")
    return AcaoSimulada(
        protocolo=f"SIM-{uuid4().hex[:8].upper()}",
        acao="cancelamento",
        pedido_id=pedido_id,
        executada=False,
        mensagem=(
            "Simulacao registrada. Nenhum pedido foi alterado; "
            "um atendente humano deve revisar a solicitacao."
        ),
        criado_em=datetime.now(UTC).isoformat(),
    )
