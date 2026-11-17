import pytest

from tests_support import validar_nome_banco_teste


@pytest.mark.parametrize("nome", ["foodagent", "postgres", "", "foodagent_test_extra"])
def test_bloqueia_banco_que_nao_seja_o_de_testes(nome):
    with pytest.raises(ValueError):
        validar_nome_banco_teste(nome)


def test_aceita_somente_banco_de_testes():
    assert validar_nome_banco_teste("foodagent_test") == "foodagent_test"
