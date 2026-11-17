import os

import psycopg
import pytest

from banco import abrir_conexao
from config import carregar_configuracao
from tests_support import validar_nome_banco_teste


@pytest.fixture
def banco_teste(monkeypatch):
    carregar_configuracao()
    nome = os.getenv("DB_TEST_NAME", "foodagent_test").strip()
    try:
        validar_nome_banco_teste(nome)
    except ValueError:
        pytest.fail(
            "Banco de integracao deve ser exatamente foodagent_test.", pytrace=False
        )

    monkeypatch.setenv("DB_NAME", nome)
    monkeypatch.setenv("APP_ENV", "test")

    try:
        with abrir_conexao() as conexao, conexao.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user")
            banco, usuario = cursor.fetchone()
            if banco != "foodagent_test" or usuario != "foodagent_app":
                pytest.fail(
                    "Conexao de teste deve usar foodagent_test e foodagent_app.",
                    pytrace=False,
                )
            cursor.execute("SELECT id, status FROM public.pedidos ORDER BY id")
            pedidos = dict(cursor.fetchall())
    except (psycopg.Error, ValueError):
        pytest.fail(
            "PostgreSQL de teste indisponivel. Consulte docs/testes-postgresql.md.",
            pytrace=False,
        )

    if pedidos.get("PED-901") != "em preparo" or pedidos.get("PED-902") != "entregue":
        pytest.fail(
            "Prepare os dados com sql/002_preparar_banco_testes.sql.", pytrace=False
        )
