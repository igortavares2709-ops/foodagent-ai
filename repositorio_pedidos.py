from schemas import PedidoResponse

_PEDIDOS_FICTICIOS = {
    "PED-001": PedidoResponse(id="PED-001", status="em preparo"),
    "PED-002": PedidoResponse(id="PED-002", status="entregue"),
}


def buscar_pedido(pedido_id: str) -> PedidoResponse | None:
    """Busca um pedido fictício sem permitir alterações no registro original."""
    pedido = _PEDIDOS_FICTICIOS.get(pedido_id)

    if pedido is None:
        return None

    return pedido.model_copy(deep=True)
