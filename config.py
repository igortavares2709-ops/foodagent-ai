import os
from pathlib import Path

from dotenv import load_dotenv


def carregar_configuracao() -> tuple[str, str]:
    """Carrega e valida as configurações básicas do projeto."""
    caminho_env = Path(__file__).resolve().parent / ".env"
    load_dotenv(caminho_env, override=False)

    ambiente = os.getenv("APP_ENV", "development").strip()
    nivel_log = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    if ambiente not in {"development", "test", "production"}:
        raise ValueError("APP_ENV deve ser development, test ou production.")

    if nivel_log not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ValueError("LOG_LEVEL contém um nível inválido.")

    return ambiente, nivel_log


if __name__ == "__main__":
    try:
        ambiente, nivel_log = carregar_configuracao()
    except ValueError as erro:
        print(f"Erro de configuração: {erro}")
        raise SystemExit(1) from None

    print(f"Ambiente: {ambiente}")
    print(f"Nível de log: {nivel_log}")
