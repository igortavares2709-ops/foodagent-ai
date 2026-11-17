"""Inicializa o PostgreSQL gerenciado com dados fictícios idempotentes."""

from pathlib import Path

from banco import abrir_conexao

ARQUIVO_SQL = Path(__file__).resolve().parents[1] / "sql" / "003_docker_init.sql"


def main() -> None:
    sql = ARQUIVO_SQL.read_text(encoding="utf-8")

    with abrir_conexao() as conexao, conexao.cursor() as cursor:
        cursor.execute(sql)

    print("Banco inicializado com sucesso.")


if __name__ == "__main__":
    main()
