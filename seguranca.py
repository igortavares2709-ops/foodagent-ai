"""Controles simples de seguranca para entradas e saidas do agente."""

import re

_PADROES_INJECAO = (
    r"ignore (todas|as|all).*(instru[cç][oõ]es|instructions)",
    r"revele.*(prompt|segredo|chave)",
    r"system prompt",
    r"developer message",
)
_EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_TELEFONE = re.compile(
    r"(?<!\d)(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}(?!\d)"
)
_CPF = re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)")


def detectar_injecao(texto: str) -> bool:
    normalizado = texto.casefold()
    return any(re.search(padrao, normalizado) for padrao in _PADROES_INJECAO)


def mascarar_dados_pessoais(texto: str) -> str:
    texto = _EMAIL.sub("[EMAIL_PROTEGIDO]", texto)
    texto = _TELEFONE.sub("[TELEFONE_PROTEGIDO]", texto)
    return _CPF.sub("[CPF_PROTEGIDO]", texto)
