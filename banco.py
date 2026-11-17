import os

import psycopg

from config import carregar_configuracao


def abrir_conexao() -> psycopg.Connection:
    """Abre uma conexão usando as configurações locais."""
    carregar_configuracao()

    senha = os.getenv("DB_PASSWORD", "")
    if not senha:
        raise ValueError("DB_PASSWORD não foi configurada no .env.")

    try:
        porta = int(os.getenv("DB_PORT", "5432"))
    except ValueError:
        raise ValueError("DB_PORT deve ser um número inteiro.") from None

    if not 1 <= porta <= 65535:
        raise ValueError("DB_PORT deve estar entre 1 e 65535.")

    return psycopg.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=porta,
        dbname=os.getenv("DB_NAME", "foodagent"),
        user=os.getenv("DB_USER", "foodagent_app"),
        password=senha,
        connect_timeout=5,
    )


def main() -> None:
    """Verifica a conexão sem mostrar credenciais."""
    try:
        with abrir_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT current_database(), current_user;")
                resultado = cursor.fetchone()
    except ValueError as erro:
        print(f"Erro de configuração: {erro}")
        raise SystemExit(1) from None
    except psycopg.Error:
        print(
            "Não foi possível acessar o PostgreSQL. "
            "Confira o serviço, as configurações e a senha no .env."
        )
        raise SystemExit(1) from None

    if resultado is None:
        print("A consulta não retornou o resultado esperado.")
        raise SystemExit(1)

    print(f"Banco conectado: {resultado[0]}")
    print(f"Usuário conectado: {resultado[1]}")


if __name__ == "__main__":
    main()