import asyncio

import httpx

from api import app


def consultar_rota(caminho):
    async def executar():
        transporte = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transporte,
            base_url="http://teste",
        ) as cliente:
            return await cliente.get(caminho)

    return asyncio.run(executar())


def test_health_retorna_status_e_aplicacao():
    resposta = consultar_rota("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "ok",
        "application": "FoodAgent AI",
    }


def test_consulta_pedido_existente():
    resposta = consultar_rota("/pedidos/PED-001")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "id": "PED-001",
        "status": "em preparo",
    }


def test_pedido_inexistente_retorna_404():
    resposta = consultar_rota("/pedidos/PED-999")

    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Pedido não encontrado."}


def test_identificador_invalido_retorna_422():
    resposta = consultar_rota("/pedidos/abc")

    assert resposta.status_code == 422

    erro = resposta.json()["detail"][0]
    assert erro["loc"] == ["path", "pedido_id"]
    assert erro["type"] == "string_pattern_mismatch"