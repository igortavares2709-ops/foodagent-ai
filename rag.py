"""RAG local e deterministico para politicas ficticias de delivery."""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from pathlib import Path

_DIMENSAO = 256
_TOKEN = re.compile(r"[a-zA-ZÀ-ÿ0-9]+")


@dataclass(frozen=True)
class Trecho:
    fonte: str
    titulo: str
    conteudo: str
    vetor: tuple[float, ...]


def _tokens(texto: str) -> list[str]:
    return [token.casefold() for token in _TOKEN.findall(texto) if len(token) > 2]


def embedding(texto: str) -> tuple[float, ...]:
    """Cria vetor local por hashing; reproduzivel e sem API externa."""
    vetor = [0.0] * _DIMENSAO
    for token in _tokens(texto):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        indice = int.from_bytes(digest[:4], "big") % _DIMENSAO
        sinal = 1.0 if digest[4] % 2 == 0 else -1.0
        vetor[indice] += sinal
    norma = math.sqrt(sum(valor * valor for valor in vetor)) or 1.0
    return tuple(valor / norma for valor in vetor)


def _similaridade(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def carregar_base(diretorio: Path | None = None) -> list[Trecho]:
    base = diretorio or Path(__file__).resolve().parent / "docs" / "politicas"
    trechos: list[Trecho] = []
    for caminho in sorted(base.glob("*.md")):
        titulo = caminho.stem.replace("-", " ").title()
        blocos = re.split(r"\n(?=## )", caminho.read_text(encoding="utf-8"))
        for bloco in blocos:
            conteudo = bloco.strip()
            if conteudo:
                cabecalho = conteudo.splitlines()[0].lstrip("# ").strip() or titulo
                trechos.append(
                    Trecho(caminho.name, cabecalho, conteudo, embedding(conteudo))
                )
    return trechos


def recuperar(pergunta: str, *, limite: int = 3) -> list[Trecho]:
    consulta = embedding(pergunta)
    candidatos = sorted(
        carregar_base(),
        key=lambda trecho: _similaridade(consulta, trecho.vetor),
        reverse=True,
    )
    return candidatos[:limite]
