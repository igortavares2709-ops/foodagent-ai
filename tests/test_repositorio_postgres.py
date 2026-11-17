from unittest.mock import MagicMock

import psycopg
import pytest

from repositorio_postgres import buscar_pedido_postgres


@pytest.fixture
def cursor_simulado(monkeypatch):
    cursor = MagicMock()
    conexao = MagicMock()

    conexao.__enter__.return_value = conexao
    conexao.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(
        "repositorio_postgres.abrir_conexao",
        lambda: conexao,
    )

    return cursor


def test_retorna_pedido_encontrado(cursor_simulado):
    cursor_simulado.fetchone.return_value = ("PED-001", "em preparo")

    pedido = buscar_pedido_postgres("PED-001")

    assert pedido is not None
    assert pedido.id == "PED-001"
    assert pedido.status == "em preparo"

    cursor_simulado.execute.assert_called_once_with(
        "SELECT id, status FROM public.pedidos WHERE id = %s",
        ("PED-001",),
    )


def test_retorna_none_para_pedido_inexistente(cursor_simulado):
    cursor_simulado.fetchone.return_value = None

    assert buscar_pedido_postgres("PED-999") is None


def test_falha_no_banco_nao_vira_pedido_inexistente(cursor_simulado):
    cursor_simulado.execute.side_effect = psycopg.OperationalError(
        "Falha simulada."
    )

    with pytest.raises(psycopg.OperationalError):
        buscar_pedido_postgres("PED-001")