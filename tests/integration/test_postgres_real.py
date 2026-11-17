import asyncio

import httpx
import pytest

from api import app
from banco import abrir_conexao
from repositorio_postgres import buscar_pedido_postgres

pytestmark = pytest.mark.integration


def consultar_api(caminho):
    async def executar():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://teste",
        ) as cliente:
            return await cliente.get(caminho)

    return asyncio.run(executar())


@pytest.mark.usefixtures("banco_teste")
def test_repositorio_consulta_pedido_persistido():
    pedido = buscar_pedido_postgres("PED-901")
    assert pedido is not None
    assert pedido.id == "PED-901"
    assert pedido.status == "em preparo"


@pytest.mark.usefixtures("banco_teste")
def test_repositorio_retorna_none_para_pedido_ausente():
    assert buscar_pedido_postgres("PED-999") is None


@pytest.mark.usefixtures("banco_teste")
def test_sql_parametrizado_nao_interpreta_entrada_como_comando():
    assert buscar_pedido_postgres("PED-901' OR '1'='1") is None


@pytest.mark.usefixtures("banco_teste")
def test_api_consulta_postgres_sem_substituir_dependencias():
    assert not app.dependency_overrides
    resposta = consultar_api("/pedidos/PED-901")
    assert resposta.status_code == 200
    assert resposta.json() == {"id": "PED-901", "status": "em preparo"}


@pytest.mark.usefixtures("banco_teste")
def test_api_pedido_ausente_no_postgres_retorna_404():
    resposta = consultar_api("/pedidos/PED-999")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Pedido n\u00e3o encontrado."}


@pytest.mark.usefixtures("banco_teste")
def test_api_rejeita_id_invalido_com_banco_configurado():
    assert consultar_api("/pedidos/abc").status_code == 422


@pytest.mark.usefixtures("banco_teste")
def test_usuario_aplicacao_tem_apenas_leitura_na_tabela():
    with abrir_conexao() as conexao, conexao.cursor() as cursor:
        cursor.execute(
            "SELECT has_table_privilege(current_user, 'public.pedidos', 'SELECT'), "
            "has_table_privilege(current_user, 'public.pedidos', 'INSERT'), "
            "has_table_privilege(current_user, 'public.pedidos', 'UPDATE'), "
            "has_table_privilege(current_user, 'public.pedidos', 'DELETE'), "
            "(SELECT rolsuper FROM pg_roles WHERE rolname = current_user)"
        )
        assert cursor.fetchone() == (True, False, False, False, False)
