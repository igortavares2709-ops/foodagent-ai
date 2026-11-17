import pytest

from ferramentas import simular_cancelamento


def test_cancelamento_e_apenas_simulado():
    acao = simular_cancelamento("PED-001", "Cliente mudou de ideia")
    assert acao.pedido_id == "PED-001"
    assert acao.executada is False
    assert acao.protocolo.startswith("SIM-")


def test_cancelamento_exige_motivo():
    with pytest.raises(ValueError):
        simular_cancelamento("PED-001", "   ")
