def main() -> None:
    """Apresenta o projeto e um pedido fictício."""
    pedido = {
        "id": "PED-001",
        "cliente": "Cliente Exemplo",
        "status": "em preparo",
    }

    print("FoodAgent AI — atendimento de delivery")
    print(f"Pedido: {pedido['id']}")
    print(f"Cliente: {pedido['cliente']}")
    print(f"Status: {pedido['status']}")


if __name__ == "__main__":
    main()
    