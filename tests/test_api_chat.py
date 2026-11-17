import asyncio

import httpx

import api


def requisitar(metodo, caminho, **kwargs):
    async def executar():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api.app),
            base_url="http://teste",
        ) as cliente:
            return await cliente.request(metodo, caminho, **kwargs)

    return asyncio.run(executar())


def test_chat_retorna_resposta_e_request_id(monkeypatch):
    monkeypatch.setattr(
        api,
        "atender",
        lambda mensagem, pedido_id: {
            "resposta": "Resposta simulada.",
            "intencao": "politica",
            "fontes": ["politica.md#Teste"],
            "requer_humano": False,
        },
    )
    resposta = requisitar(
        "POST",
        "/chat",
        json={"mensagem": "Qual é a política?"},
        headers={"X-Request-ID": "req-teste"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["request_id"] == "req-teste"
    assert resposta.headers["X-Request-ID"] == "req-teste"


def test_chat_valida_mensagem_vazia():
    assert requisitar("POST", "/chat", json={"mensagem": ""}).status_code == 422


def test_cancelamento_retorna_simulacao():
    resposta = requisitar(
        "POST",
        "/acoes/cancelamento",
        json={"pedido_id": "PED-001", "motivo": "Mudança de planos"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["executada"] is False


def test_metricas_sao_expostas():
    resposta = requisitar("GET", "/metrics")
    assert resposta.status_code == 200
    assert resposta.json()["requisicoes"] >= 1
