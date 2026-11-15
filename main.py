from config import carregar_configuracao


def main() -> None:
    """Valida a configuração e apresenta um pedido fictício."""
    try:
        ambiente, nivel_log = carregar_configuracao()
    except ValueError as erro:
        print(f"Erro de configuração: {erro}")
        raise SystemExit(1) from None

    pedido = {
        "id": "PED-001",
        "cliente": "Cliente Exemplo",
        "status": "em preparo",
    }

    print("FoodAgent AI — atendimento de delivery")
    print(f"Ambiente: {ambiente}")
    print(f"Nível de log: {nivel_log}")
    print(f"Pedido: {pedido['id']}")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Status: {pedido['status']}")


if __name__ == "__main__":
    main()