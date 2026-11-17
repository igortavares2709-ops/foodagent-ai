from repositorio_pedidos import buscar_pedido


def test_busca_pedido_existente():
    pedido = buscar_pedido("PED-001")

    assert pedido is not None
    assert pedido.id == "PED-001"
    assert pedido.status == "em preparo"


def test_pedido_inexistente_retorna_none():
    assert buscar_pedido("PED-999") is None


def test_alterar_copia_nao_modifica_pedido_armazenado():
    pedido = buscar_pedido("PED-001")
    assert pedido is not None

    pedido.status = "entregue"

    nova_consulta = buscar_pedido("PED-001")
    assert nova_consulta is not None
    assert nova_consulta.status == "em preparo"
