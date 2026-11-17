"""Prepara apenas o PostgreSQL efemero do GitHub Actions."""

import os
from pathlib import Path

import psycopg
from psycopg import sql


def main() -> None:
    if os.getenv("CI") != "true":
        raise SystemExit("Ferramenta exclusiva do ambiente efemero de CI.")
    senha_admin = os.environ["CI_POSTGRES_PASSWORD"]
    senha_app = os.environ["DB_PASSWORD"]
    with (
        psycopg.connect(
            host="127.0.0.1",
            port=5432,
            dbname="foodagent_test",
            user="postgres",
            password=senha_admin,
            connect_timeout=5,
        ) as conexao,
        conexao.cursor() as cursor,
    ):
        cursor.execute("SELECT current_database()")
        if cursor.fetchone()[0] != "foodagent_test":
            raise SystemExit("Banco incorreto.")
        cursor.execute(
            sql.SQL("CREATE ROLE foodagent_app LOGIN PASSWORD {}").format(
                sql.Literal(senha_app)
            )
        )
        caminho = (
            Path(__file__).resolve().parents[1] / "sql/002_preparar_banco_testes.sql"
        )
        cursor.execute(caminho.read_text(encoding="utf-8"))
    print("Banco efemero de integracao preparado.")


if __name__ == "__main__":
    main()
