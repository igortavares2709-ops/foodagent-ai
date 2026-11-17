import psycopg

from banco import abrir_conexao
from schemas import PedidoResponse


def buscar_pedido_postgres(pedido_id: str) -> PedidoResponse | None:
    """Consulta um pedido no PostgreSQL usando parâmetros seguros."""
    with abrir_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT id, status FROM public.pedidos WHERE id = %s",
                (pedido_id,),
            )
            registro = cursor.fetchone()

    if registro is None:
        return None

    return PedidoResponse(id=registro[0], status=registro[1])


def main() -> None:
    try:
        pedido = buscar_pedido_postgres("PED-001")
    except ValueError:
        print("Configuração ou dados inválidos. Confira a configuração local.")
        raise SystemExit(1) from None
    except psycopg.Error:
        print("Falha ao consultar pedidos no PostgreSQL.")
        raise SystemExit(1) from None

    if pedido is None:
        print("Pedido não encontrado.")
    else:
        print(f"Pedido: {pedido.id}")
        print(f"Status: {pedido.status}")


if __name__ == "__main__":
    main()