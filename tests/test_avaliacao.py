import agente
import avaliar


def test_avaliacao_deterministica(monkeypatch):
    monkeypatch.setattr(
        agente,
        "consultar_status",
        lambda pedido_id: type(
            "Pedido", (), {"id": pedido_id, "status": "em preparo"}
        )(),
    )
    monkeypatch.setattr(avaliar, "atender", agente.atender)
    resultado = avaliar.executar()
    assert resultado["total"] == 4
    assert resultado["taxa"] == 1.0
