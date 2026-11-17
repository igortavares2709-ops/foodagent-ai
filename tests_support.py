def validar_nome_banco_teste(nome: str) -> str:
    """Protege ferramentas de teste contra acesso ao banco da aplicacao."""
    if nome != "foodagent_test":
        raise ValueError("Banco de integracao deve ser exatamente foodagent_test.")
    return nome
