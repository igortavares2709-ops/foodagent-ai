import asyncio

import httpx

from api import app


def test_health_retorna_status_e_aplicacao():
    async def consultar_health():
        transporte = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transporte,
            base_url="http://teste",
        ) as cliente:
            return await cliente.get("/health")

    resposta = asyncio.run(consultar_health())

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "ok",
        "application": "FoodAgent AI",
    }