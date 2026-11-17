from rag import carregar_base, embedding, recuperar


def test_embedding_e_deterministico_e_normalizado():
    primeiro = embedding("atraso na entrega")
    segundo = embedding("atraso na entrega")
    assert primeiro == segundo
    assert 0.99 <= sum(x * x for x in primeiro) <= 1.01


def test_carrega_documentos_de_politicas():
    fontes = {trecho.fonte for trecho in carregar_base()}
    assert {"cancelamento.md", "entrega.md", "reembolso.md"} <= fontes


def test_recupera_politica_de_atraso():
    resultados = recuperar("minha entrega está atrasada", limite=2)
    assert resultados
    assert any("Atrasos" in trecho.titulo for trecho in resultados)
