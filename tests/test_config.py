import pytest

from config import carregar_configuracao


@pytest.fixture(autouse=True)
def isolar_configuracao(monkeypatch):
    """Impede que os testes leiam o .env real."""
    monkeypatch.setattr("config.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)


def test_usa_valores_padrao():
    assert carregar_configuracao() == ("development", "INFO")


def test_aceita_configuracao_valida(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    assert carregar_configuracao() == ("test", "DEBUG")


def test_rejeita_ambiente_invalido(monkeypatch):
    monkeypatch.setenv("APP_ENV", "invalido")

    with pytest.raises(ValueError, match="APP_ENV"):
        carregar_configuracao()


def test_rejeita_nivel_log_invalido(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "INVALIDO")

    with pytest.raises(ValueError, match="LOG_LEVEL"):
        carregar_configuracao()